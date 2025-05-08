import math

# 示例输入：订单列表 orders 和原材料列表 raws
orders = [
    #（高度、宽度、数量、单位利润）
    # (height, width, quantity, unit_profit)
    (2.2, 1.6, 10, 480.0),  # 订单1：单价480元，每套需4根材料，每根利润120元
    (2.4, 1.8, 20, 680.0),  # 订单2：单价680元，每根利润170元
    (2.3, 1.7, 20, 550.0),  # 订单3：单价550元，每根利润137.5元
    (2.0, 1.5, 15, 420.0),   # 订单4：单价420元，每根利润105元
    # 可根据实际需求扩充
]
raws = [
    # (长度，成本，缺陷列表)，缺陷列表为(开始，长度) 的列表
    # (length, cost, defect_list), defect_list 为 (start, length) 的列表
    (5.5, 18.0, [(1.0, 0.03), (2.5, 0.04)]),
    (6.2, 22.0, [(0.5, 0.02), (1.8, 0.05)]),
    (7.8, 28.0, [(3.0, 0.03)]),
    # 可根据实际原料类型扩充
]
kerf = 0.005  # 锯口宽度 (米)
tolerance = 0.01  # 长度容差 (米)

# 展开订单需求为边长列表
demand_pieces = []
total_revenue = 0.0
for h, w, qty, profit in orders:
    total_revenue += profit * qty
    # 每套窗框需2根高度边和2根宽度边
    demand_pieces += [h] * (2*qty) + [w] * (2*qty)

# 初始化结果统计
used_raw_count = [0] * len(raws)  # 每种原材用量
total_cost = 0.0
total_kerf_loss = 0.0
# 实际切割出的总长度（供计算利用率）
actual_cut_length = 0.0

# 转换剩余需求为列表，随切割更新
remaining = demand_pieces.copy()

# 主循环：当需求仍未满足时，每轮选择一个原材切割模式
while remaining:
    best_score = -1.0
    best_choice = None
    # 针对每种原材模拟最佳切割模式
    for i, (raw_len, raw_cost, defects) in enumerate(raws):
        # 生成此原材的可用段列表（去除缺陷）
        segments = []
        last = 0.0
        for d_start, d_len in sorted(defects, key=lambda x: x[0]):
            if d_start > last:
                segments.append(d_start - last)
            last = d_start + d_len
        if last < raw_len:
            segments.append(raw_len - last)
        if not segments:
            continue
        segments.sort(reverse=True)  # 优先尝试最长段
        # 复制需求列表进行模拟
        sim_remain = sorted(remaining, reverse=True)
        pieces_chosen = []  # 记录此次模拟要切的件原始需求长度
        sim_used_length = 0.0
        sim_kerf = 0.0
        # 对每个段进行贪心装载
        for seg_len in segments:
            seg_remain = seg_len
            first_piece = True
            # 当前段内循环装件
            while True:
                # 切除锯口（若非首件）
                if not first_piece:
                    seg_remain -= kerf
                    sim_kerf += kerf
                first_piece = False
                if seg_remain < 0:
                    break
                # 找到一个能装下的最大件
                found = False
                for idx, piece in enumerate(sim_remain):
                    L = piece
                    # 判断此段剩余是否能放下一个件（考虑容差）
                    if seg_remain >= L + tolerance:
                        # 普通剪切情况：切出长度 L
                        pieces_chosen.append(L)
                        sim_used_length += L
                        seg_remain -= L
                        del sim_remain[idx]
                        found = True
                        break
                    elif seg_remain >= L - tolerance:
                        # 剩余段稍短于 L，但在容差内，可全部切断段
                        pieces_chosen.append(L)
                        sim_used_length += seg_remain  # 实际切出段剩余长度
                        del sim_remain[idx]
                        seg_remain = 0.0
                        found = True
                        break
                if not found:
                    break  # 当前段无法再装下任何件
        # 计算得分：使用长度与成本比率
        score = sim_used_length / raw_cost if raw_cost > 0 else 0
        if score > best_score and sim_used_length > 0:
            best_score = score
            best_choice = (i, pieces_chosen, sim_used_length)
    # 如果没有任何原材能装入，跳出
    if best_choice is None:
        print("无法满足剩余需求，请检查原材是否足够。")
        break
    # 应用最优切割模式：更新需求和统计量
    idx, chosen_pieces, used_len = best_choice
    raw_len, raw_cost, defects = raws[idx]
    used_raw_count[idx] += 1
    total_cost += raw_cost
    # 重新计算切割过程以统计锯口损耗和剩余
    # （与模拟过程一致）
    segments = []
    last = 0.0
    for d_start, d_len in sorted(defects, key=lambda x: x[0]):
        if d_start > last:
            segments.append(d_start - last)
        last = d_start + d_len
    if last < raw_len:
        segments.append(raw_len - last)
    segments.sort(reverse=True)
    seg_remain_list = []
    # 模拟分段再次切割，计算锯口并记录实际切出长度
    seg_remain_list = []
    sim_remain = sorted(remaining, reverse=True)
    actual_used = 0.0
    kerf_loss = 0.0
    for seg_len in segments:
        seg_remain = seg_len
        first_piece = True
        while True:
            if not first_piece:
                seg_remain -= kerf
                kerf_loss += kerf
            first_piece = False
            if seg_remain < 0:
                break
            found = False
            for j, piece in enumerate(sim_remain):
                L = piece
                if seg_remain >= L + tolerance:
                    # 切出长度 L
                    actual_used += L
                    seg_remain -= L
                    del sim_remain[j]
                    found = True
                    break
                elif seg_remain >= L - tolerance:
                    # 切出剩余段全长
                    actual_used += seg_remain
                    del sim_remain[j]
                    seg_remain = 0.0
                    found = True
                    break
            if not found:
                break
    # 剩余需求更新
    # 注意：无论实际切长，需求都按原始长度移除件
    for L in chosen_pieces:
        # 从 remaining 中删除一个等长需求
        if L in remaining:
            remaining.remove(L)
    total_kerf_loss += kerf_loss
    actual_cut_length += actual_used

# 计算结果
total_revenue = total_revenue
profit = total_revenue - total_cost
material_used_length = sum([raws[i][0] * used_raw_count[i] for i in range(len(raws))])
utilization = (actual_cut_length / material_used_length * 100) if material_used_length > 0 else 0

# 输出结果
print(f"最大利润: {profit:.2f} 单位")
print(f"材料利用率: {utilization:.2f}%")
print(f"总锯口损耗长度: {total_kerf_loss:.3f} 米")
# 余料 = 用材总长 - 实际切割长度 - 锯口损耗
leftover = material_used_length - actual_cut_length - total_kerf_loss
print(f"总余料长度: {leftover:.3f} 米")
for i, cnt in enumerate(used_raw_count):
    print(f"原材料类型 {i} 使用数量: {cnt}")
