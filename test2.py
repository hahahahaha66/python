#问题一代码
import pulp
import itertools

# --------------------------
# 参数设定（可修改）
# --------------------------

saw_kerf = 0.005  # 锯口宽度

orders = {
    1: {"width": 1.6, "height": 2.2, "tolerance": 0.01, "quantity": 10, "price": 480},
    2: {"width": 1.8, "height": 2.4, "tolerance": 0.01, "quantity": 20, "price": 680},
    3: {"width": 1.7, "height": 2.3, "tolerance": 0.01, "quantity": 20, "price": 550},
    4: {"width": 1.5, "height": 2.0, "tolerance": 0.01, "quantity": 15, "price": 420},
}

materials = {
    1: {"length": 5.5, "cost": 18},
    2: {"length": 6.2, "cost": 22},
    3: {"length": 7.8, "cost": 28},
}

# --------------------------
# 边长收集
# --------------------------

edges = {}
for k, v in orders.items():
    edges[(k, 'W')] = (v['width'], v['price'])
    edges[(k, 'H')] = (v['height'], v['price'])

# --------------------------
# 枚举所有切割模式
# --------------------------

def generate_patterns(material_len):
    patterns = []
    for counts in itertools.product(range(0, 6), repeat=8):  # 最多切 5 根边，8 种边
        total_len = 0
        total_cuts = sum(counts)
        if total_cuts == 0:
            continue
        for idx, count in enumerate(counts):
            edge_len = list(edges.values())[idx][0]
            total_len += count * edge_len
        total_len += (total_cuts - 1) * saw_kerf
        if total_len <= material_len:
            pattern = {}
            for i, key in enumerate(edges.keys()):
                if counts[i] > 0:
                    pattern[key] = counts[i]
            patterns.append((pattern, total_len))
    return patterns

# --------------------------
# 建立模型
# --------------------------

model = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

pattern_vars = {}
all_patterns = {}

for mat_id, mat in materials.items():
    mat_patterns = generate_patterns(mat["length"])
    for j, (pat, used_len) in enumerate(mat_patterns):
        var = pulp.LpVariable(f"x_{mat_id}_{j}", lowBound=0, cat="Integer")
        pattern_vars[(mat_id, j)] = var
        all_patterns[(mat_id, j)] = {"pattern": pat, "used_len": used_len}

order_vars = {}
for k in orders:
    order_vars[k] = pulp.LpVariable(f"y_{k}", lowBound=0, upBound=orders[k]["quantity"], cat="Integer")

# --------------------------
# 目标函数
# --------------------------

revenue = sum(order_vars[k] * orders[k]["price"] for k in orders)
cost = sum(pattern_vars[(i, j)] * materials[i]["cost"] for (i, j) in pattern_vars)
model += (revenue - cost)

# --------------------------
# 约束条件
# --------------------------

for k in orders:
    total_width = sum(pattern_vars[(i, j)] * pat["pattern"].get((k, 'W'), 0)
                      for (i, j), pat in all_patterns.items())
    total_height = sum(pattern_vars[(i, j)] * pat["pattern"].get((k, 'H'), 0)
                       for (i, j), pat in all_patterns.items())
    model += (total_width >= 2 * order_vars[k])
    model += (total_height >= 2 * order_vars[k])

# --------------------------
# 求解模型
# --------------------------

solver = pulp.PULP_CBC_CMD()
model.solve(solver)

# --------------------------
# 输出结果
# --------------------------

print(f"状态: {pulp.LpStatus[model.status]}")
print(f"最大利润: {pulp.value(model.objective)} 元\n")

for k in orders:
    print(f"订单{k}：完成 {int(order_vars[k].varValue)} 套")

print("\n使用的原材料组合：")
total_material_cost = 0
total_used_len = 0
total_saw_loss = 0
for (i, j), var in pattern_vars.items():
    count = var.varValue
    if count > 0:
        pattern = all_patterns[(i, j)]["pattern"]
        used_len = all_patterns[(i, j)]["used_len"]
        saw_loss = (sum(pattern.values()) - 1) * saw_kerf
        print(f"材料{i}, 模式{j}, 使用次数: {int(count)}, 总长: {used_len:.3f} 米, 模式: {pattern}")
        total_material_cost += count * materials[i]["cost"]
        total_used_len += count * used_len
        total_saw_loss += count * saw_loss

# --------------------------
# 考虑边角浪费后的利用率计算
# --------------------------

min_edge_len = min(length for length, _ in edges.values())
edge_scrap_loss = 0.0
for (i, j), var in pattern_vars.items():
    count = var.varValue
    if count > 0:
        mat_len = materials[i]["length"]
        used_len = all_patterns[(i, j)]["used_len"]
        leftover = mat_len - used_len
        if leftover < min_edge_len + saw_kerf:
            edge_scrap_loss += leftover * count

print(f"\n总原材料长度使用: {total_used_len:.3f} 米")
print(f"总锯口损失: {total_saw_loss:.3f} 米")
print(f"总边角浪费: {edge_scrap_loss:.3f} 米")

total_real_loss = total_saw_loss + edge_scrap_loss
print(f"切割利用率: {(total_used_len - total_real_loss) / total_used_len:.2%}")
print(f"总损失率（锯口 + 边角浪费）: {total_real_loss / total_used_len:.2%}")
