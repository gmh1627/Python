import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import pdfkit

# 1. 使用 Pyppeteer 获取渲染后的网页
async def get_page_content(url):
    browser = await launch(headless=True, executablePath='C:/Program Files/Google/Chrome/Application/chrome.exe')
    page = await browser.newPage()
    await page.goto(url, {"waitUntil": "networkidle2"})  # 确保动态内容加载完毕
    content = await page.content()  # 获取页面内容
    await browser.close()
    return content

# 2. 提取指定标签内容
def extract_article(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    main_tag = soup.find("main", {"role": "main", "class": "App-main"})
    if main_tag:
        article_tag = main_tag.find("article", {"class": "Post-Main Post-NormalMain"})
        if article_tag:
            return str(article_tag)  # 返回 <article> 部分的 HTML 内容
    return None

# 3. 将 HTML 内容保存为 PDF，指定中文字体
def save_to_pdf(html_content, output_pdf_path):
    # 为 HTML 添加一个简单的 CSS 样式，指定字体
    css = '''
    <style>
        body {
            font-family: 'SimSun', "KaiTi", "Arial", sans-serif;
        }
    </style>
    '''
    html_with_css = css + html_content  # 将 CSS 添加到 HTML 中
    options = {
        'encoding': 'UTF-8',
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'javascript-delay': '3000',
    }
    pdfkit.from_string(html_with_css, output_pdf_path, options=options)

# 主函数：执行整个过程
async def main():
    url = "https://zhuanlan.zhihu.com/p/695832406"
    html_content = await get_page_content(url)
    article_content = extract_article(html_content)
    if article_content:
        output_pdf_path = "zhihu_article.pdf"
        save_to_pdf(article_content, output_pdf_path)
        print(f"PDF saved as {output_pdf_path}")
    else:
        print("Failed to extract the article content.")

# 运行主函数
asyncio.get_event_loop().run_until_complete(main())