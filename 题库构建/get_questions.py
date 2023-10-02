# 导入库
from bs4 import BeautifulSoup
import re

'''
/html/body/p[1]
/html/body/p[2]
/html/body/p[3]
/html/body/p[4]
/html/body/p[5]
'''

def answer_extract(text):
    # 使用正则表达式匹配题目类型、题目、选项和正确答案
    match = re.match(r'^\d+、单选题：(.+?)选项：(.+?)答案: 【(.+?)】', text)

    if match:
        # 提取匹配的信息
        question = match.group(1)
        options_str = match.group(2)
        answer = match.group(3)

        # 使用正则表达式分割选项字符串
        options = re.findall(r'[A-D]:\s*([^A-D]+)', options_str)

        # 输出提取的信息
        # print("题目:", question)
        # print("选项:", options)
        # print("正确答案:", answer)
        return {
            "question": question,
            "options": options,
            "correct_answers": answer
        }
    else:
        return None
        # print("未找到匹配的信息")


# 打开本地 HTML 文件
with open('answers.html', 'r', encoding='utf-8') as file:
    html_doc = file.read()

# 创建 BeautifulSoup 对象并指定解析器（可以使用内置的 'html.parser'）
soup = BeautifulSoup(html_doc, 'html.parser')

ps = soup.find_all("p")

answers = []

for p in ps:
    # print(p.text)
    text_temp=re.sub(r'\u200d|\u200e|\u200f|\u200b|\u200c|\xa0', '', p.text)
    # print(answer_extract(text_temp))
    answers.append(answer_extract(text_temp))


# 将JSON数据写入文件（可选）
with open("answers.txt", "w" ,encoding='utf-8') as txt_file:
    txt_file.write(str(answers))


