import pandas as pd

# 读取原始 JSON 文件和生成的 CSV 文件
json_data = pd.read_json('outbox.json')
csv_data = pd.read_csv('output.csv')

# 获取原始 JSON 数据中的唯一标识符列表
json_ids = json_data['id'].tolist()

# 获取生成的 CSV 数据中的唯一标识符列表
csv_ids = csv_data['id'].tolist()

# 比较唯一标识符列表，找出在原始 JSON 中存在但在 CSV 中缺失的标识符
missing_ids = set(json_ids) - set(csv_ids)

# 打印缺失的标识符
print("Missing IDs:")
for id in missing_ids:
    print(id)
