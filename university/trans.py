import json

# 读取JSON文件，并处理整个文件内容
with open('university.json', 'r', encoding='utf-8') as file:
    # 读取整个文件内容
    data = json.load(file)
    
    # 逐个处理JSON对象
    for item in data:
        # 提取所需的信息
        name = item['name']
        university = item['university']
        
        # 将提取的信息写入TXT文件
        output_text = f"{name} {university}\n"
        
        # 打开输出文件，并追加内容
        with open('湛江一中2022届毕业去向.txt', 'a', encoding='utf-8') as output_file:
            output_file.write(output_text)