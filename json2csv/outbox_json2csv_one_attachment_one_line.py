import pandas as pd
import json

# 文件路径
file_path = "outbox.json"

# 打开并读取JSON文件
with open(file_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# 打印一些数据以检查其结构
# for item in json_data['orderedItems'][:5]:  # 只查看前5个项目
#     print(json.dumps(item, indent=4))  # 使用json.dumps以格式化的方式打印

# 先检查 object 是否包含 attachment 字段，如果不存在则赋值为空数组。这样可以确保每一个 object 都有 attachment 字段，即使它是空的
for item in json_data['orderedItems']:
    if 'object' in item:
        if isinstance(item['object'], str):
            try:
                item['object'] = json.loads(item['object'])
            except json.JSONDecodeError:
                item['object'] = {}

        if 'attachment' not in item['object']:
            item['object']['attachment'] = []
    else:
        item['object'] = {}

# 将 JSON 数据扁平化
df = pd.json_normalize(json_data['orderedItems'], 
                       record_path=['object', 'attachment'],
                       meta=['id', ['object', 'id'], ['object', 'type'], ['object', 'published'], ['object', 'url'],
                             ['object', 'content'], ['object', 'inReplyTo'],
                             ['signature', 'creator'], ['signature', 'created'], ['signature', 'signatureValue']],
                       errors='ignore')

# 将 DataFrame 转换为 CSV 文件
df.to_csv('output.csv', index=False)
