import pandas as pd
import json

# 文件路径
file_path = "outbox.json"

# 打开并读取 JSON 文件
with open(file_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# 先检查 object 是否为列表类型，如果不是则转换为包含该对象的列表
for item in json_data['orderedItems']:
    if 'object' in item:
        if not isinstance(item['object'], list):
            item['object'] = [item['object']]
        for obj in item['object']:
            if isinstance(obj, str):
                try:
                    obj = json.loads(obj)
                except json.JSONDecodeError:
                    obj = {}

            if 'attachment' not in obj:
                obj['attachment'] = []

            # 处理 attachment
            attachments = obj['attachment']
            attachment_html = ''.join([f'<img src="{attachment["url"]}">' for attachment in attachments])

            # 处理 inReplyTo
            in_reply_to = obj.get('inReplyTo')
            in_reply_to_html = f'<!-- wp:indieblocks/context --><div class="wp-block-indieblocks-context"><i>In reply to <a class="u-in-reply-to" href="{in_reply_to}">{in_reply_to}</a>.</i></div><!-- /wp:indieblocks/context -->' if in_reply_to else ''

            # 处理 content
            content = obj.get('content', '')
            processed_content = f'{in_reply_to_html}{content}{attachment_html}'

            obj['content'] = processed_content

# 提取所有字段并添加到记录中
data = []
for item in json_data['orderedItems']:
    for obj in item['object']:
        if isinstance(obj, dict):  # 添加类型检查
            record = {
                'id': item['id'],
                'type': obj['type'],
                'summary': obj.get('summary', ''),
                'content': obj.get('content', ''),
                'lang': ', '.join(obj.get('contentMap', {}).keys())
            }
            for key, value in obj.items():
                if key not in ['type', 'summary', 'content', 'contentMap']:
                    record[key] = value
            data.append(record)

# 创建 DataFrame
df = pd.DataFrame(data)

# 将 DataFrame 转换为 CSV 文件
df.to_csv('output.csv', index=False)
