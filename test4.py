#依旧太慢
import pulp
import itertools

# --------------------------
# 参数设定
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

defect_info = {
    1: [(1.0, 0.03), (2.5, 0.04)],
    2: [(0.5, 0.02), (1.8, 0.05)],
    3: [(3.0, 0.03)]
}

# --------------------------
# 边长收集
# --------------------------

edges = {}
for k, v in orders.items():
    edges[(k, 'W')] = (v['width'], v['price'])
    edges[(k, 'H')] = (v['height'], v['price'])

# --------------------------
# 判断是否与缺陷重叠
# --------------------------

def overlaps_with_defects(start, length, defects):
    for defect_start, defect_len in defects:
        defect_end = defect_start + defect_len
        if not (start + length <= defect_start or start >= defect_end):
            return True
    return False

# --------------------------
# 模式生成，含剪枝优化
# --------------------------

def generate_patterns_with_defects(material_len, defects):
    patterns = []
    edge_items = list(edges.items())

    for counts in itertools.product(range(0, 6), repeat=len(edge_items)):
        total_pieces = sum(counts)
        if total_pieces == 0 or total_pieces > 6:
            continue

        segment_positions = []
        pos = 0.0
        valid = True
        for i, count in enumerate(counts):
            edge_len = edge_items[i][1][0]
            for _ in range(count):
                total_len = edge_len + saw_kerf if segment_positions else edge_len
                while overlaps_with_defects(pos, total_len, defects):
                    pos += 0.01
                    if pos + total_len > material_len:
                        valid = False
                        break
                if not valid or pos + total_len > material_len:
                    valid = False
                    break
                segment_positions.append((pos, total_len))
                pos += total_len
            if not valid:
                break

        if valid:
            used_len = pos
            utilization = used_len / material_len
            if utilization < 0.6:
                continue  # 剪枝：跳过低利用率模式

            pattern = {}
            for i, key in enumerate(edge_items):
                if counts[i] > 0:
                    pattern[key[0]] = counts[i]
            patterns.append((pattern, used_len))
    return patterns

# --------------------------
# 建立模型
# --------------------------

model = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

pattern_vars = {}
all_patterns = {}

for mat_id, mat in materials.items():
    mat_patterns = generate_patterns_with_defects(mat["length"], defect_info.get(mat_id, []))
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
# 利用率分析
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
