import pulp

# —————————————————————————————————————————
# 一、输入数据
# —————————————————————————————————————————

# 订单数据（表3）
orders = [
    {"id": 1, "qty": 120, "width": 1.6, "height": 2.2, "price": 480},
    {"id": 2, "qty": 80,  "width": 1.8, "height": 2.4, "price": 680},
    {"id": 3, "qty": 60,  "width": 1.7, "height": 2.3, "price": 550},
    {"id": 4, "qty": 40,  "width": 1.5, "height": 2.0, "price": 420},
]

# 原材料数据（已修正）

materials = [
    {"id": 1, "length": 5.5, "cost": 17.00, "defects": [(1.0, 0.3)]},
    {"id": 2, "length": 5.5, "cost": 17.33, "defects": [(3.0, 0.2)]},
    {"id": 3, "length": 6.2, "cost": 20.59, "defects": [(2.0, 0.4)]},
    {"id": 4, "length": 7.0, "cost": 24.41, "defects": [(1.5, 0.2)]},
    {"id": 5, "length": 7.0, "cost": 24.05, "defects": [(4.0, 0.3)]},
    {"id": 6, "length": 5.8, "cost": 17.33, "defects": [(1.2, 0.5)]},
    {"id": 7, "length": 6.5, "cost": 22.00, "defects": [(2.3, 0.3)]},
    {"id": 8, "length": 7.5, "cost": 24.77, "defects": [(1.0, 0.6)]},
    {"id": 9, "length": 6.0, "cost": 19.83, "defects": [(2.8, 0.4)]},
    {"id": 10, "length": 8.2, "cost": 27.64, "defects": [(1.3, 0.5)]},
    {"id": 11, "length": 6.8, "cost": 23.32, "defects": [(2.1, 0.3)]},
    {"id": 12, "length": 6.8, "cost": 23.69, "defects": [(5.0, 0.2)]},
    {"id": 13, "length": 5.6, "cost": 17.66, "defects": [(1.1, 0.2)]},
    {"id": 14, "length": 7.3, "cost": 24.77, "defects": [(3.1, 0.4)]},
    {"id": 15, "length": 6.1, "cost": 19.83, "defects": [(1.7, 0.5)]},
    {"id": 16, "length": 8.0, "cost": 27.64, "defects": [(2.5, 0.3)]},
    {"id": 17, "length": 5.9, "cost": 18.00, "defects": [(3.0, 0.4)]},
    {"id": 18, "length": 6.3, "cost": 21.27, "defects": [(1.9, 0.3)]},
    {"id": 19, "length": 7.8, "cost": 26.57, "defects": [(1.2, 0.4)]},
    {"id": 20, "length": 6.7, "cost": 22.91, "defects": [(2.4, 0.3)]},
    {"id": 21, "length": 5.4, "cost": 16.68, "defects": [(0.8, 0.3)]},
    {"id": 22, "length": 7.4, "cost": 25.85, "defects": [(3.0, 0.2)]},
    {"id": 23, "length": 6.9, "cost": 22.91, "defects": [(2.0, 0.5)]},
    {"id": 24, "length": 8.1, "cost": 27.64, "defects": [(2.2, 0.4)]},
    {"id": 25, "length": 7.6, "cost": 26.20, "defects": [(1.6, 0.3)]},
    {"id": 26, "length": 5.7, "cost": 17.33, "defects": [(2.7, 0.4)]},
    {"id": 27, "length": 6.4, "cost": 22.00, "defects": [(1.8, 0.2)]},
    {"id": 28, "length": 8.3, "cost": 28.72, "defects": [(0.9, 0.3)]},
    {"id": 29, "length": 6.0, "cost": 18.00, "defects": [(1.1, 0.5)]},
    {"id": 30, "length": 7.9, "cost": 27.64, "defects": [(2.9, 0.2)]},
    {"id": 31, "length": 5.5, "cost": 16.68, "defects": [(1.3, 0.4)]},
    {"id": 32, "length": 6.2, "cost": 20.95, "defects": [(3.2, 0.3)]},
    {"id": 33, "length": 7.1, "cost": 23.69, "defects": [(2.3, 0.5)]},
    {"id": 34, "length": 6.8, "cost": 23.69, "defects": [(1.9, 0.2)]},
    {"id": 35, "length": 5.8, "cost": 17.66, "defects": [(2.5, 0.4)]},
    {"id": 36, "length": 7.3, "cost": 25.13, "defects": [(3.0, 0.3)]},
    {"id": 37, "length": 6.9, "cost": 24.05, "defects": [(2.0, 0.2)]},
    {"id": 38, "length": 7.5, "cost": 25.49, "defects": [(1.6, 0.4)]},
    {"id": 39, "length": 5.6, "cost": 17.33, "defects": [(1.0, 0.3)]},
    {"id": 40, "length": 6.4, "cost": 20.95, "defects": [(2.2, 0.5)]},
    {"id": 41, "length": 6.6, "cost": 22.00, "defects": [(2.0, 0.4)]},
    {"id": 42, "length": 7.0, "cost": 24.05, "defects": [(3.1, 0.3)]},
    {"id": 43, "length": 8.0, "cost": 28.00, "defects": [(1.5, 0.2)]},
    {"id": 44, "length": 5.9, "cost": 19.83, "defects": [(1.9, 0.3)]},
    {"id": 45, "length": 7.7, "cost": 25.85, "defects": [(2.6, 0.5)]},
    {"id": 46, "length": 6.5, "cost": 22.41, "defects": [(1.1, 0.2)]},
    {"id": 47, "length": 7.2, "cost": 24.41, "defects": [(2.7, 0.4)]},
    {"id": 48, "length": 6.1, "cost": 20.59, "defects": [(3.0, 0.3)]},
    {"id": 49, "length": 5.4, "cost": 17.00, "defects": [(1.5, 0.2)]},
    {"id": 50, "length": 8.2, "cost": 27.64, "defects": [(2.0, 0.5)]},
    {"id": 51, "length": 6.7, "cost": 22.91, "defects": [(2.9, 0.3)]},
    {"id": 52, "length": 7.8, "cost": 26.57, "defects": [(1.2, 0.4)]},
    {"id": 53, "length": 5.5, "cost": 16.36, "defects": [(2.1, 0.5)]},
    {"id": 54, "length": 6.6, "cost": 22.00, "defects": [(3.2, 0.4)]},
    {"id": 55, "length": 7.0, "cost": 24.05, "defects": [(1.7, 0.3)]},
    {"id": 56, "length": 5.8, "cost": 17.66, "defects": [(1.0, 0.4)]},
    {"id": 57, "length": 8.0, "cost": 28.00, "defects": [(2.3, 0.2)]},
    {"id": 58, "length": 6.9, "cost": 23.69, "defects": [(2.5, 0.3)]},
    {"id": 59, "length": 7.2, "cost": 24.41, "defects": [(3.0, 0.4)]},
    {"id": 60, "length": 6.3, "cost": 21.27, "defects": [(2.4, 0.3)]},
    {"id": 61, "length": 8.1, "cost": 27.27, "defects": [(1.9, 0.5)]},
    {"id": 62, "length": 5.6, "cost": 17.00, "defects": [(3.1, 0.4)]},
    {"id": 63, "length": 7.4, "cost": 25.49, "defects": [(2.0, 0.3)]},
    {"id": 64, "length": 6.1, "cost": 19.83, "defects": [(1.8, 0.5)]},
    {"id": 65, "length": 6.8, "cost": 23.69, "defects": [(2.1, 0.2)]},
    {"id": 66, "length": 7.3, "cost": 25.13, "defects": [(1.4, 0.3)]},
    {"id": 67, "length": 5.7, "cost": 17.33, "defects": [(2.6, 0.4)]},
    {"id": 68, "length": 7.0, "cost": 24.41, "defects": [(2.5, 0.2)]},
    {"id": 69, "length": 6.5, "cost": 22.00, "defects": [(3.0, 0.3)]},
    {"id": 70, "length": 5.8, "cost": 17.33, "defects": [(1.2, 0.5)]},
    {"id": 71, "length": 8.2, "cost": 28.00, "defects": [(2.7, 0.4)]},
    {"id": 72, "length": 7.5, "cost": 25.85, "defects": [(3.0, 0.3)]},
    {"id": 73, "length": 6.0, "cost": 19.41, "defects": [(1.1, 0.3)]},
    {"id": 74, "length": 7.7, "cost": 25.85, "defects": [(2.3, 0.5)]},
    {"id": 75, "length": 6.6, "cost": 22.00, "defects": [(2.0, 0.4)]},
    {"id": 76, "length": 6.2, "cost": 21.27, "defects": [(3.1, 0.2)]},
    {"id": 77, "length": 7.3, "cost": 25.13, "defects": [(1.5, 0.3)]},
    {"id": 78, "length": 5.5, "cost": 16.68, "defects": [(2.4, 0.4)]},
    {"id": 79, "length": 7.0, "cost": 23.32, "defects": [(1.8, 0.5)]},
    {"id": 80, "length": 6.9, "cost": 23.69, "defects": [(2.5, 0.3)]},
]

kerf = 0.005  # 锯口宽度

# —————————————————————————————————————————
# 二、预处理：生成可用区间
# —————————————————————————————————————————
def split_segments(mat):
    defects = sorted(mat["defects"], key=lambda x: x[0])
    segments = []
    prev = 0.0
    L = mat["length"]
    
    for pos, dlen in defects:
        if pos > prev:
            segments.append((prev, pos))
        prev = pos + dlen
    if prev < L:
        segments.append((prev, L))
    
    return [s for s in segments if s[1]-s[0] >= 0.1]  # 最小切割长度0.1米

for m in materials:
    m["segments"] = split_segments(m)

# —————————————————————————————————————————
# 三、生成切割模式
# —————————————————————————————————————————
patterns = []
for m_idx, m in enumerate(materials):
    for seg in m["segments"]:
        seg_len = seg[1] - seg[0]
        
        # 处理宽度需求
        for o in orders:
            w_lo = o["width"] - 0.01
            w_hi = o["width"] + 0.01
            max_w = int((seg_len + kerf) // (w_hi + kerf))
            for nw in range(1, max_w+1):
                used_w = nw * w_hi + (nw-1)*kerf
                if used_w <= seg_len:
                    patterns.append({
                        "type": "W",
                        "mid": m["id"],
                        "oid": o["id"],
                        "qty": nw,
                        "len": used_w,
                        "price": o["price"]  # 完整订单价格
                    })
        
        # 处理高度需求
        for o in orders:
            h_lo = o["height"] - 0.01
            h_hi = o["height"] + 0.01
            max_h = int((seg_len + kerf) // (h_hi + kerf))
            for nh in range(1, max_h+1):
                used_h = nh * h_hi + (nh-1)*kerf
                if used_h <= seg_len:
                    patterns.append({
                        "type": "H",
                        "mid": m["id"],
                        "oid": o["id"],
                        "qty": nh,
                        "len": used_h,
                        "price": o["price"]
                    })

# —————————————————————————————————————————
# 四、建立MIP模型
# —————————————————————————————————————————
prob = pulp.LpProblem("Opt3", pulp.LpMaximize)

# 变量定义
x = pulp.LpVariable.dicts("Pattern", range(len(patterns)), 0, cat="Integer")
y = pulp.LpVariable.dicts("Material", [m["id"] for m in materials], 0, 1, cat="Binary")

# 目标函数：总收益 - 总成本
revenue = pulp.lpSum(x[p].qty * x[p].price for p in range(len(patterns)))
cost = pulp.lpSum(y[m] * materials[m-1]["cost"] for m in [m["id"] for m in materials])
prob += revenue - cost

# 约束1：每个订单的宽高需求
for o in orders:
    # 宽度约束
    prob += pulp.lpSum(
        x[p].qty * (1 if p.pattern["type"]=="W" and p.pattern["oid"]==o["id"] else 0)
        for p in range(len(patterns))
    ) >= 2 * o["qty"]
    
    # 高度约束
    prob += pulp.lpSum(
        x[p].qty * (1 if p.pattern["type"]=="H" and p.pattern["oid"]==o["id"] else 0)
        for p in range(len(patterns))
    ) >= 2 * o["qty"]

# 约束2：材料使用限制
for m in materials:
    prob += pulp.lpSum(
        x[p].qty * x[p].len
        for p in range(len(patterns))
        if x[p].mid == m["id"]
    ) <= m["length"] * y[m["id"]]

# 约束3：材料启用与模式使用关联
for p in range(len(patterns)):
    prob += x[p].qty <= pulp.lpSum(
        y[m["id"]] 
        for m in materials 
        if m["id"] == patterns[p].mid
    )

# —————————————————————————————————————————
# 五、求解与输出
# —————————————————————————————————————————
prob.solve(pulp.PULP_CBC_CMD(msg=False))

# 状态检查
print("Status:", pulp.LpStatus[prob.status])
if pulp.LpStatus[prob.status] != "Optimal":
    print("未找到最优解！")
    exit()

# 计算指标
total_mat = sum(y[m["id"]].varValue * m["length"] for m in materials)
total_used = sum(x[p].varValue * x[p].len for p in range(len(patterns)))
utilization = (total_used / total_mat * 100) if total_mat > 0 else 0

# 输出结果
print(f"\n最优总利润：{pulp.value(prob.objective):.2f} 元")
print(f"总用料量：{total_mat:.3f} 米")
print(f"总使用量：{total_used:.3f} 米")
print(f"材料利用率：{utilization:.2f}%")

# 输出切割方案
print("\n切割方案：")
for p in range(len(patterns)):
    if x[p].varValue > 0:
        print(f"材料{patterns[p].mid} → 订单{patterns[p].oid} {patterns[p].type}×{patterns[p].qty} ×{int(x[p].varValue)}次")