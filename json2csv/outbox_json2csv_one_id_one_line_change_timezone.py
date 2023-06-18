import pandas as pd
import json
from datetime import datetime, timedelta

# 文件路径
file_path = "output.csv"

# 读取 CSV 文件
df = pd.read_csv(file_path)

# 转换时间。(hours=9)即给待处理的时间戳加9个钟头。可修改为自己所需要的
df['published'] = pd.to_datetime(df['published']) + timedelta(hours=9)

# 将 DataFrame 转换为 CSV 文件
df.to_csv('output_utc9.csv', index=False)
