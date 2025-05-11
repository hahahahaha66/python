import pulp
import numpy as np

# 输入数据定义
materials = [
    {
        'id': 1,
        'length': 5.5,
        'defects': [[1.0, 0.03], [2.5, 0.04]],
        'price': 18
    },
    {
        'id': 2,
        'length': 6.2,
        'defects': [[0.5, 0.02], [1.8, 0.05]],
        'price': 22
    },
    {
        'id': 3,
        'length': 7.8,
        'defects': [[3.0, 0.03]],
        'price': 28
    }
]

orders = [
    [1, 10, 1.6, 2.2, 480],   # 学校教学楼
    [2, 20, 1.8, 2.4, 680],   # 酒店客房
    [3, 20, 1.7, 2.3, 550],   # 医院病房
    [4, 15, 1.5, 2.0, 420]    # 政府办公楼
]

kerf = 0.005
min_segment_length = 0.1

# 步骤1：预处理原材料，分割可用子段
def preprocess_materials(materials):
    for mat in materials:
        defects = sorted(mat['defects'], key=lambda x: x[0])
        L = mat['length']
        segments = []
        prev_end = 0.0
        
        for d in defects:
            start = d[0]
            length = d[1]
            end = start + length
            
            if start > prev_end:
                segments.append([prev_end, start])
            prev_end = end
        
        if prev_end < L:
            segments.append([prev_end, L])
        
        # 过滤有效子段
        valid_segments = []
        for seg in segments:
            if seg[1] - seg[0] >= min_segment_length:
                valid_segments.append(seg)
        
        mat['segments'] = valid_segments

preprocess_materials(materials)

# 步骤2：生成所有可行切割模式
patterns = []

for mat_idx, mat in enumerate(materials):
    for seg in mat['segments']:
        seg_start, seg_end = seg
        seg_length = seg_end - seg_start
        
        for order in orders:
            order_id, quantity, width, height, price = order
            w_min = width - 0.01
            w_max = width + 0.01
            h_min = height - 0.01
            h_max = height + 0.01
            
            # 生成宽段模式
            max_w = int((seg_length + kerf) // (w_min + kerf))
            for w in range(1, max_w + 1):
                total_kerf = kerf * (w - 1)
                required_length = w * w_max + total_kerf
                if required_length <= seg_length:
                    patterns.append({
                        'material': mat_idx,
                        'segment': (seg_start, seg_end),
                        'order': order_id - 1,  # 转为0-based索引
                        'type': 'width',
                        'quantity': w,
                        'length_used': required_length,
                        'price': mat['price']
                    })
            
            # 生成高段模式
            max_h = int((seg_length + kerf) // (h_min + kerf))
            for h in range(1, max_h + 1):
                total_kerf = kerf * (h - 1)
                required_length = h * h_max + total_kerf
                if required_length <= seg_length:
                    patterns.append({
                        'material': mat_idx,
                        'segment': (seg_start, seg_end),
                        'order': order_id - 1,  # 转为0-based索引
                        'type': 'height',
                        'quantity': h,
                        'length_used': required_length,
                        'price': mat['price']
                    })

# 步骤3：建立整数线性规划模型
prob = pulp.LpProblem("Cutting_Optimization", pulp.LpMinimize)

# 创建决策变量
x = [pulp.LpVariable(f'x{i}', lowBound=0, cat='Integer') for i in range(len(patterns))]

# 目标函数：总成本
prob += pulp.lpSum(x[i] * patterns[i]['price'] for i in range(len(patterns)))

# 需求约束（每个订单需要2宽+2高）
num_orders = len(orders)
demand_constraints = np.zeros((2*num_orders, len(patterns)), dtype=int)

for i, pattern in enumerate(patterns):
    order_idx = pattern['order']
    if pattern['type'] == 'width':
        row = order_idx
    else:
        row = num_orders + order_idx
    demand_constraints[row, i] = pattern['quantity']

for row in range(2*num_orders):
    order_idx = row % num_orders
    required = 2 * orders[order_idx][1]
    prob += pulp.lpSum(demand_constraints[row, i] * x[i] for i in range(len(patterns))) >= required

# 求解问题
prob.solve()

# 步骤4：结果分析
if pulp.LpStatus[prob.status] == 'Optimal':
    print("\n========= 优化结果 =========")
    
    # 提取解决方案
    solution = [int(var.value()) for var in x]
    used_patterns = [i for i in range(len(patterns)) if solution[i] > 0]
    
    # 计算总成本
    total_cost = sum(solution[i] * patterns[i]['price'] for i in range(len(patterns)))
    
    # 计算总收益
    total_revenue = sum(order[1] * order[4] for order in orders)
    
    # 计算材料使用量
    material_usage = [0] * len(materials)
    total_used_length = 0.0
    for i in used_patterns:
        material_usage[patterns[i]['material']] += solution[i]
        total_used_length += solution[i] * patterns[i]['length_used']
    
    # 计算总材料长度
    total_material_length = sum(materials[i]['length'] * material_usage[i] for i in range(len(materials)))
    
    # 计算利用率
    utilization = total_used_length / total_material_length * 100
    loss_rate = 100 - utilization
    
    # 打印结果
    print(f"总成本: {total_cost}元")
    print(f"总收益: {total_revenue}元")
    print(f"利润: {total_revenue - total_cost}元")
    print(f"材料利用率: {utilization:.2f}%")
    print(f"切割损失率: {loss_rate:.2f}%")
    
    # 打印切割方案详情
    print("\n========= 切割方案详情 =========")
    for mat_idx in range(len(materials)):
        print(f"\n原材料{mat_idx+1}（长度{materials[mat_idx]['length']}米）:")
        for i in used_patterns:
            if patterns[i]['material'] == mat_idx and solution[i] > 0:
                seg = patterns[i]['segment']
                print(f"  子段[{seg[0]:.2f}-{seg[1]:.2f}] → "
                      f"订单{patterns[i]['order']+1}的{patterns[i]['type']}×{patterns[i]['quantity']} "
                      f"(使用次数: {solution[i]})")
else:
    print("未找到可行解！")