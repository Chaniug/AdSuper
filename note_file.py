import os
import time

# 获取当前日期和时间组合的数据
current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())

# 读取原始文件内容
with open("AdSuper.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# 创建一个新的列表，用于存储更新后的内容
updated_lines = []

# 遍历原始文件的每一行
for line in lines:
    # 如果行中包含 "Version" 字符串
    if "Version: " in line:
        # 获取 "Version" 后面的日期和时间组合数据
        date_time = line.split("Version: ")[-1].strip()
        # 将日期和时间组合数据更新为当前的日期和时间组合数据
        updated_line = line.replace(date_time, f"{current_time}")
    else:
        # 如果行中不包含 "Version" 字符串，则直接将该行添加到新的列表中
        updated_line = line
    # 将更新后的行添加到新的列表中
    updated_lines.append(updated_line)

# 将更新后的内容写入原始文件
with open("AdSuper.txt", "w", encoding="utf-8") as f:
    f.writelines(updated_lines)
