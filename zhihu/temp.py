import json
import os
import re
from jinja2 import Environment, FileSystemLoader
import requests
import pdfkit

# 用户输入专栏名称，默认为c_1747690982282477569
column_id = input("请输入知乎专栏ID（默认为 c_1747690982282477569）：") or 'c_1747690982282477569'
url = f'https://www.zhihu.com/api/v4/columns/{column_id}/articles'

# 发送请求获取专栏文章列表
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 解析 JSON 数据
    data = response.json()
    
    # 保存到本地文件
    output_file = 'zhihu.json'
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    print(f"数据已保存到 {output_file}")
else:
    print(f"请求失败，状态码：{response.status_code}")

def process_content(content):
    """
    处理HTML内容，移除不需要的标签和属性，调整样式等。
    """
    # 移除标识符号
    # 匹配 data-pid 属性，并允许属性值使用普通双引号或转义的双引号，以及可能存在的空白字符
    content = re.sub(r'data-pid\s*=\s*(?:"|\")(.+?)(?:"|\")', '', content)
    
    # 替换特殊字符
    content = content.replace('\u003C', '<').replace('\u003E', '>')
    
    # 处理<p>标签，添加缩进和底部边距
    content = content.replace('<p ', '<p style="text-indent: 2em; margin-bottom: 1em;">')
    
    # 处理</p>标签
    content = content.replace('</p>', '</p>')
    
    # 移除包含 <img> 的 <figure> 标签
    content = re.sub(r'<figure.*?>.*?</figure>', '', content, flags=re.DOTALL)
    
    # 移除 class="ztext-empty-paragraph"
    content = re.sub(r'<p[^>]*class\s*=\s*["\']ztext-empty-paragraph["\'][^>]*>', '</p>', content)
    
    # 去除多余的<br>
    content = re.sub(r'</p><br>', '</p>', content)
    
    # 最后一个段落不应该有额外的换行
    if content.endswith('<p style="text-indent: 2em; margin-bottom: 1em;">'):
        content = content[:-len('<p style="text-indent: 2em; margin-bottom: 1em;">')]
    content += '</p>'
    
    # 确保每段文本都包裹在<p>和</p>之间
    paragraphs = re.split(r'(<p[^>]*>)', content)
    cleaned_paragraphs = []
    for i in range(0, len(paragraphs), 2):
        if i + 1 < len(paragraphs):  # 如果有对应的<p>标签
            cleaned_paragraphs.append(paragraphs[i])
            cleaned_paragraphs.append(paragraphs[i + 1].strip())
        else:
            cleaned_paragraphs.append(paragraphs[i].strip())
    
    content = ''.join(cleaned_paragraphs)
    
    return content

# 定义输入文件名
input_file = 'zhihu.json'

# 从文件中读取JSON数据
with open(input_file, 'r', encoding='utf-8') as file:
    json_data = file.read()

# 解析JSON数据
data = json.loads(json_data)

# 提取"data"数组中的内容
articles_data = data['data']

# 创建一个目录来保存HTML和PDF文件
output_dir = 'articles'
os.makedirs(output_dir, exist_ok=True)

# 初始化Jinja2环境
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.html')

# 遍历每一篇文章的数据
for article in articles_data:
    # 获取文章内容和标题
    article_id = str(article['id'])
    content = article['content']
    processed_content = process_content(content)
    title = article['title']
    
    # 渲染HTML模板
    html_content = template.render(title=title, content=processed_content)
    
    # 移除连续的 '>>'，只保留一个 '>'
    html_content = re.sub(r'(>)>', r'\1', html_content)
    
    # 将内容写入HTML文件
    html_file_path = os.path.join(output_dir, f'{article_id}.html')
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

print("所有文章已保存为HTML文件")

# 指定输入文件夹
input_dir = 'articles'

# 创建一个目录来保存 PDF 文件
output_dir = 'pdfs'
os.makedirs(output_dir, exist_ok=True)

# 遍历文件夹中的所有 HTML 文件
for filename in os.listdir(input_dir):
    if filename.endswith('.html'):
        # 获取 HTML 文件的完整路径
        html_file_path = os.path.join(input_dir, filename)
        
        # 构造 PDF 文件的名称
        pdf_filename = os.path.splitext(filename)[0] + '.pdf'
        pdf_file_path = os.path.join(output_dir, pdf_filename)
        
        # 读取 HTML 文件内容
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # 将 HTML 文件转换为 PDF 文件
        try:
            # 使用 options 禁止加载远程资源
            options = {
                'disable-local-file-access': None,
                'load-error-handling': 'ignore',
            }
            # 注意html文件名不能含有中文
            pdfkit.from_string(html_content, pdf_file_path, options=options)
            print(f"{filename} 已转换为 {pdf_filename}")
        except Exception as e:
            print(f"转换 {filename} 时发生错误：{e}")

print("所有 HTML 文件已转换为 PDF 文件。")