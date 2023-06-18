import json
from lxml import etree
import random
import string

import requests
from bs4 import BeautifulSoup


def generate_random_uuid():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


def convert_to_wordpress_xml(data):
    rss = etree.Element('{http://purl.org/rss/1.0/}rss', version="2.0")
    channel = etree.SubElement(rss, 'channel')

    for record in data:
        item = etree.SubElement(channel, 'item')
        title = etree.SubElement(item, 'title')
        title.text = '标题 Title'  # post标题，可修改为你所要的

        creator = etree.SubElement(item, 'creator')
        creator.text = '作者 author'  # post作者，可修改为你所要的

        content_encoded = etree.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded')
        content = '<!-- wp:indieblocks/like --><div class="wp-block-indieblocks-like"><div class="u-like-of h-cite"><p><i>Likes <a class="u-url" href="{record}">a toot</a>.</i></p></div></div> <!-- /wp:indieblocks/like -->'
        # post样式，可修改为你所要的
        # 目前有生成xml中content会HTML转义的问题。但是并不影响导入。
        content_encoded.text = content.format(record=record)

        post_name = etree.SubElement(item, 'post_name')
        post_name.text = generate_random_uuid()

        status = etree.SubElement(item, 'status')
        status.text = 'private'  # post可见状态

        post_type = etree.SubElement(item, 'post_type')
        post_type.text = 'indieblocks_like'  # post类型，可修改为你所要的

    tree = etree.ElementTree(rss)
    return tree


def save_to_multiple_files(data, batch_size):
    total_items = len(data)
    num_files = total_items // batch_size + 1

    for i in range(num_files):
        start = i * batch_size
        end = min(start + batch_size, total_items)
        batch_data = data[start:end]

        # 转换为 WordPress XML
        wordpress_xml = convert_to_wordpress_xml(batch_data)

        # 保存为 XML 文件
        filename = f'likes_batch_{i + 1}.xml'
        wordpress_xml.write(filename, encoding='utf-8', xml_declaration=True, pretty_print=True)
        print(f'Saved {filename} with {len(batch_data)} items')


# 读取 JSON 数据
with open('likes.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)
items = json_data['orderedItems']

# 是否保存为多个 XML 文件的开关
save_to_multiple = False

# 每个文件包含的记录数量
batch_size = 1000

# 是否更新 post_date 字段的开关
update_post_date = True

# 转换为 WordPress XML
wordpress_xml = convert_to_wordpress_xml(items)

if save_to_multiple:
    # 保存为多个 XML 文件
    save_to_multiple_files(items, batch_size)
else:
    # 保存为单个 XML 文件
    wordpress_xml.write('likes.xml', encoding='utf-8', xml_declaration=True, pretty_print=True)

    if update_post_date:
        # 读取 WordPress XML 文件
        tree = etree.parse('likes.xml')

        # 命名空间映射
        namespaces = {
            'content': 'http://purl.org/rss/1.0/modules/content/',
            'wp': 'http://wordpress.org/export/1.2/'
        }

        # 获取根元素
        root = tree.getroot()

        # 遍历每个 item
        for item in root.findall('channel/item'):
            # 获取链接
            link = item.find('{http://purl.org/rss/1.0/modules/content/}encoded').text
            soup = BeautifulSoup(link, 'html.parser')
            url = soup.find('a', {'class': 'u-url'})['href']

            # 请求链接获取创建时间
            response = requests.get(url, verify=True)  # False代表禁用SSL证书验证。如果True值无法得到你想要的结果，可考虑。请注意，这会使请求变得不安全，因为它将接受任何证书，包括自签名证书。请确保您在安全的环境中使用这个设置。
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                time_data = soup.find('data', {'class': 'dt-published'})
                if time_data and 'value' in time_data.attrs:
                    # 更新 WordPress XML 中的 post_date
                    post_date = item.find('wp:post_date', namespaces=namespaces)
                    if post_date is not None:
                        post_date.text = time_data['value']
                    else:
                        post_date = etree.SubElement(item, '{http://wordpress.org/export/1.2/}post_date', nsmap=namespaces)
                        post_date.text = time_data['value']
                else:
                    print(f"Warning: No 'published' time found in the response from {url}")
            else:
                print(f"Error: Failed to get response from {url}, status code: {response.status_code}")

        # 保存更新后的 WordPress XML 文件
        tree.write('likes_time_updated.xml', encoding='utf-8', xml_declaration=True, pretty_print=True)
