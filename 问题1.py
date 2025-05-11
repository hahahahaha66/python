import numpy as np
from pulp import *

# —————— 输入数据 ——————
# 订单：[订单量, 宽度, 高度, 单价]
orders = np.array([
    [10, 1.6, 2.2, 480],
    [20, 1.8, 2.4, 680],
    [20, 1.7, 2.3, 550],
    [15, 1.5, 2.0, 420]
])
num_orders = orders.shape[0]

# 每种长度需求（宽 + 高），每类需求两件
lengths = np.concatenate((orders[:,1], orders[:,2]))
demands = np.concatenate((orders[:,0]*2, orders[:,0]*2))
num_types = len(lengths)

# 原料规格与单价
stock_len = np.array([5.5, 6.2, 7.8])
stock_price = np.array([18, 22, 28])
saw = 0.005

# —————— 生成所有切割组合 ——————
def compositions(n, k):
    if n == 1:
        return np.array([[k]])
    result = []
    for i in range(k + 1):
        for tail in compositions(n-1, k - i):
            result.append(np.concatenate(([i], tail)))
    return np.array(result)

patterns_all = []
rod_idx = []

for j, L in enumerate(stock_len):
    max_pieces = int((L + saw) // (min(lengths) + saw))
    for k in range(1, max_pieces + 1):
        comps = compositions(num_types, k)
        for a in comps:
            used = np.sum(a * lengths) + (np.sum(a) - 1) * saw
            if used <= L + 1e-9:
                patterns_all.append(a)
                rod_idx.append(j)

patterns_all = np.array(patterns_all)
rod_idx = np.array(rod_idx)
num_pat = len(patterns_all)

# —————— 构建 MILP ——————
prob = LpProblem("CuttingStock", LpMinimize)
y = [LpVariable(f"y_{p}", lowBound=0, cat=LpInteger) for p in range(num_pat)]

# 目标函数：总成本最小
prob += lpSum([stock_price[rod_idx[p]] * y[p] for p in range(num_pat)])

# 每种件数需求约束
for t in range(num_types):
    prob += lpSum([patterns_all[p][t] * y[p] for p in range(num_pat)]) >= demands[t]

# 求解
prob.solve(PULP_CBC_CMD(msg=0))
y_opt = np.array([int(v.varValue) for v in y])
cost_min = value(prob.objective)

# —————— 结果计算 ——————
total_revenue = np.sum(orders[:,0] * orders[:,3])
total_cost = cost_min
profit = total_revenue - total_cost

supplied_length = np.sum(y_opt * stock_len[rod_idx])
piece_length = patterns_all @ lengths
saw_usage = (np.sum(patterns_all, axis=1) - 1) * saw
used_length = np.sum(y_opt * (piece_length + saw_usage))

cut_loss = supplied_length - used_length
utilization = used_length / supplied_length * 100

# —————— 输出 ——————
print("最优切割模式及用量：")
for p, count in enumerate(y_opt):
    if count > 0:
        print(f" 模式 #{p} (原料 {stock_len[rod_idx[p]]:.1f}m)：切出 {patterns_all[p]} 件，使用 {count} 根")

print(f"\n总销售收益：{total_revenue:.2f} 元")
print(f"原材料成本：{total_cost:.2f} 元")
print(f"最大利润：{profit:.2f} 元")
print(f"供应总长度：{supplied_length:.2f} m")
print(f"有效使用长度：{used_length:.2f} m")
print(f"切割损失（含锯口+剩余）：{cut_loss:.2f} m")
print(f"材料利用率：{utilization:.2f} %")
