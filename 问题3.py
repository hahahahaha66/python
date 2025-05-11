import pulp
import numpy as np

# 输入数据定义
materials = [
    {'id': 1, 'length': 5.5, 'defects': [[1.0, 0.3]], 'price': 17.0},
    {'id': 1, 'length': 5.5, 'defects': [[3.0, 0.2]], 'price': 17.33},
    {'id': 2, 'length': 6.2, 'defects': [[2.0, 0.4]], 'price': 20.59},
    {'id': 3, 'length': 7.0, 'defects': [[1.5, 0.2]], 'price': 24.41},
    {'id': 3, 'length': 7.0, 'defects': [[4.0, 0.3]], 'price': 24.05}, 
    {'id': 4, 'length': 5.8, 'defects': [[1.2, 0.5]], 'price': 17.33},
    {'id': 5, 'length': 6.5, 'defects': [[2.3, 0.3]], 'price': 22.0}, 
    {'id': 6, 'length': 7.5, 'defects': [[1.0, 0.6]], 'price': 24.77},
    {'id': 7, 'length': 6.0, 'defects': [[2.8, 0.4]], 'price': 19.83}, 
    {'id': 8, 'length': 8.2, 'defects': [[1.3, 0.5]], 'price': 27.64},
    {'id': 9, 'length': 6.8, 'defects': [[2.1, 0.3]], 'price': 23.32}, 
    {'id': 9, 'length': 6.8, 'defects': [[5.0, 0.2]], 'price': 23.69},
    {'id': 10, 'length': 5.6, 'defects': [[1.1, 0.2]], 'price': 17.66}, 
    {'id': 11, 'length': 7.3, 'defects': [[3.1, 0.4]], 'price': 24.77},
    {'id': 12, 'length': 6.1, 'defects': [[1.7, 0.5]], 'price': 19.83}, 
    {'id': 13, 'length': 8.0, 'defects': [[2.5, 0.3]], 'price': 27.64},
    {'id': 14, 'length': 5.9, 'defects': [[3.0, 0.4]], 'price': 18.0}, 
    {'id': 15, 'length': 6.3, 'defects': [[1.9, 0.3]], 'price': 21.27},
    {'id': 16, 'length': 7.8, 'defects': [[1.2, 0.4]], 'price': 26.57}, 
    {'id': 17, 'length': 6.7, 'defects': [[2.4, 0.3]], 'price': 22.91},
    {'id': 18, 'length': 5.4, 'defects': [[0.8, 0.3]], 'price': 16.68}, 
    {'id': 19, 'length': 7.4, 'defects': [[3.0, 0.2]], 'price': 25.85},
    {'id': 20, 'length': 6.9, 'defects': [[2.0, 0.5]], 'price': 22.91}, 
    {'id': 21, 'length': 8.1, 'defects': [[2.2, 0.4]], 'price': 27.64},
    {'id': 22, 'length': 7.6, 'defects': [[1.6, 0.3]], 'price': 26.2}, 
    {'id': 23, 'length': 5.7, 'defects': [[2.7, 0.4]], 'price': 17.33},
    {'id': 24, 'length': 6.4, 'defects': [[1.8, 0.2]], 'price': 22.0}, 
    {'id': 25, 'length': 8.3, 'defects': [[0.9, 0.3]], 'price': 28.72},
    {'id': 26, 'length': 6.0, 'defects': [[1.1, 0.5]], 'price': 18.0}, 
    {'id': 27, 'length': 7.9, 'defects': [[2.9, 0.2]], 'price': 27.64},
    {'id': 28, 'length': 5.5, 'defects': [[1.3, 0.4]], 'price': 16.68}, 
    {'id': 29, 'length': 6.2, 'defects': [[3.2, 0.3]], 'price': 20.95},
    {'id': 30, 'length': 7.1, 'defects': [[2.3, 0.5]], 'price': 23.69}, 
    {'id': 31, 'length': 6.8, 'defects': [[1.9, 0.2]], 'price': 23.69},
    {'id': 32, 'length': 5.8, 'defects': [[2.5, 0.4]], 'price': 17.66}, 
    {'id': 33, 'length': 7.3, 'defects': [[3.0, 0.3]], 'price': 25.13},
    {'id': 34, 'length': 6.9, 'defects': [[2.0, 0.2]], 'price': 24.05}, 
    {'id': 35, 'length': 7.5, 'defects': [[1.6, 0.4]], 'price': 25.49},
    {'id': 36, 'length': 5.6, 'defects': [[1.0, 0.3]], 'price': 17.33}, 
    {'id': 37, 'length': 6.4, 'defects': [[2.2, 0.5]], 'price': 20.95},
    {'id': 38, 'length': 6.6, 'defects': [[2.0, 0.4]], 'price': 22.0}, 
    {'id': 39, 'length': 7.0, 'defects': [[3.1, 0.3]], 'price': 24.05},
    {'id': 40, 'length': 8.0, 'defects': [[1.5, 0.2]], 'price': 28.0}, 
    {'id': 41, 'length': 5.9, 'defects': [[1.9, 0.3]], 'price': 19.83},
    {'id': 42, 'length': 7.7, 'defects': [[2.6, 0.5]], 'price': 25.85}, 
    {'id': 43, 'length': 6.5, 'defects': [[1.1, 0.2]], 'price': 22.41},
    {'id': 44, 'length': 7.2, 'defects': [[2.7, 0.4]], 'price': 24.41}, 
    {'id': 45, 'length': 6.1, 'defects': [[3.0, 0.3]], 'price': 20.59},
    {'id': 46, 'length': 5.4, 'defects': [[1.5, 0.2]], 'price': 17.0}, 
    {'id': 47, 'length': 8.2, 'defects': [[2.0, 0.5]], 'price': 27.64},
    {'id': 48, 'length': 6.7, 'defects': [[2.9, 0.3]], 'price': 22.91}, 
    {'id': 49, 'length': 7.8, 'defects': [[1.2, 0.4]], 'price': 26.57},
    {'id': 50, 'length': 5.5, 'defects': [[2.1, 0.5]], 'price': 16.36}, 
    {'id': 51, 'length': 6.6, 'defects': [[3.2, 0.4]], 'price': 22.0},
    {'id': 52, 'length': 7.0, 'defects': [[1.7, 0.3]], 'price': 24.05}, 
    {'id': 53, 'length': 5.8, 'defects': [[1.0, 0.4]], 'price': 17.66},
    {'id': 54, 'length': 8.0, 'defects': [[2.3, 0.2]], 'price': 28.0}, 
    {'id': 55, 'length': 6.9, 'defects': [[2.5, 0.3]], 'price': 23.69},
    {'id': 56, 'length': 7.2, 'defects': [[3.0, 0.4]], 'price': 24.41}, 
    {'id': 57, 'length': 6.3, 'defects': [[2.4, 0.3]], 'price': 21.27},
    {'id': 58, 'length': 8.1, 'defects': [[1.9, 0.5]], 'price': 27.27}, 
    {'id': 59, 'length': 5.6, 'defects': [[3.1, 0.4]], 'price': 17.0},
    {'id': 60, 'length': 7.4, 'defects': [[2.0, 0.3]], 'price': 25.49}, 
    {'id': 61, 'length': 6.1, 'defects': [[1.8, 0.5]], 'price': 19.83},
    {'id': 62, 'length': 6.8, 'defects': [[2.1, 0.2]], 'price': 23.69}, 
    {'id': 63, 'length': 7.3, 'defects': [[1.4, 0.3]], 'price': 25.13},
    {'id': 64, 'length': 5.7, 'defects': [[2.6, 0.4]], 'price': 17.33}, 
    {'id': 65, 'length': 7.0, 'defects': [[2.5, 0.2]], 'price': 24.41},
    {'id': 66, 'length': 6.5, 'defects': [[3.0, 0.3]], 'price': 22.0}, 
    {'id': 67, 'length': 5.8, 'defects': [[1.2, 0.5]], 'price': 17.33},
    {'id': 68, 'length': 8.2, 'defects': [[2.7, 0.4]], 'price': 28.0}, 
    {'id': 69, 'length': 7.5, 'defects': [[3.0, 0.3]], 'price': 25.85},
    {'id': 70, 'length': 6.0, 'defects': [[1.1, 0.3]], 'price': 19.41}, 
    {'id': 71, 'length': 7.7, 'defects': [[2.3, 0.5]], 'price': 25.85},
    {'id': 72, 'length': 6.6, 'defects': [[2.0, 0.4]], 'price': 22.0}, 
    {'id': 73, 'length': 6.2, 'defects': [[3.1, 0.2]], 'price': 21.27},
    {'id': 74, 'length': 7.3, 'defects': [[1.5, 0.3]], 'price': 25.13}, 
    {'id': 75, 'length': 5.5, 'defects': [[2.4, 0.4]], 'price': 16.68},
    {'id': 76, 'length': 7.0, 'defects': [[1.8, 0.5]], 'price': 23.32}, 
    {'id': 77, 'length': 6.9, 'defects': [[2.5, 0.3]], 'price': 23.69},
    {'id': 78, 'length': 8.0, 'defects': [[2.6, 0.4]], 'price': 27.27}, 
    {'id': 79, 'length': 7.4, 'defects': [[1.7, 0.2]], 'price': 25.85},
    {'id': 80, 'length': 6.3, 'defects': [[3.0, 0.5]], 'price': 20.59},
]

orders = [
    [1, 120, 1.6, 2.2, 480],   # 学校教学楼
    [2, 80, 1.8, 2.4, 680],   # 酒店客房
    [3, 60, 1.7, 2.3, 550],   # 医院病房
    [4, 40, 1.5, 2.0, 420]    # 政府办公楼
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