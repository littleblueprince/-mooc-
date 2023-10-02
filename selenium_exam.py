# -*- coding: utf-8 -*-

import json
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import difflib

questions_json = [{'question': 'PKI通过引入____解决如何相信公钥与身份的绑定关系的问题。',
                   'options': ['密钥共享', 'SET协议', '证书', '数字签名'], 'correct_answers': '证书'},
                  {'question': '不属于PKI系统的组件的是____。', 'options': [' ', 'R', '证书发布系统', '认证服务器'],
                   'correct_answers': '认证服务器AS'}, {'question': '不属于PKI系统的典型信任模型的是____。',
                                                        'options': ['层次结构信任模型', '交叉认证',
                                                                    '网状(Mesh)信任模型', '社交网络信任模型'],
                                                        'correct_answers': '社交网络信任模型'},
                  {'question': '关于层次结构信任模型描述不正确的是____。',
                   'options': ['对于安全主体(End-Entity)而言，仅需要信任给它的签发证书的', '要维护层次结构，在每个', '根',
                               '根'],
                   'correct_answers': '对于安全主体(End-Entity)而言，仅需要信任给它的签发证书的CA或该CA的父节点CA'},
                  {'question': '以下说法不正确的是____。',
                   'options': ['交叉认证包括单向交叉认证和双向交叉认证', 'R', '交叉认证时可能会有路径长度约束',
                               '无论层次结构信任模型还是交叉认证，要完成证书的验证，都需要证书链上的所有证书的签名验证都通过'],
                   'correct_answers': 'RA可作为层次结构信任模型的叶节点'},
                  {'question': '以下说法不正确的是____。', 'options': ['没有到期的证书不会被提前撤销', ' ', ' ', ' '],
                   'correct_answers': '没有到期的证书不会被提前撤销'},
                  {'question': '_____算法只能用于实现密钥交换，算法的安全性依赖于有限域上的离散对数问题。（ ）',
                   'options': [' ', '椭圆曲线公钥密码', 'RS', ' '], 'correct_answers': 'Diffie-Hellman'},
                  {'question': '下面关于公开密钥密码体制，不正确的是（ ）。',
                   'options': ['加密与解密由不同的密钥完成，并且可以交换使用。', '通信双方掌握的秘密信息(密钥)是一样的。',
                               '若知道加密算法，从加密密钥得到解密密钥在计算上是不可行的。',
                               '一般情况下，公钥密码加密和解密速度较对称密钥密码慢。'],
                   'correct_answers': '通信双方掌握的秘密信息(密钥)是一样的。'}, {
                      'question': '1976年，Diffie和Hellman在论文“密码学新方向（New Direction in Cryptography）”中首次提出了公开密钥密码体制的思想；“公开密钥密码体制”的意思是（  ）。',
                      'options': ['将公钥和私钥都公开', '将公钥公开,将私钥保密', '将私钥公开,将公钥保密',
                                  '将公钥和私钥都保密'], 'correct_answers': '将公钥公开,将私钥保密'},
                  {'question': '以下哪项不是分组加密算法？（ ）', 'options': ['RS', ' ', ' ', 'R'],
                   'correct_answers': 'RC4'}, {'question': '以下哪些不属于RSA算法的应用（ ）。',
                                               'options': ['数据加密', '密钥交换', '数字签名', '可靠传输'],
                                               'correct_answers': '可靠传输'},
                  {'question': '比特币的两个主要支撑技术是（ ）。',
                   'options': ['区块链和公开密钥技术', '区块链和P2P网络', '数字签名和哈希算法', '账本和匿名性'],
                   'correct_answers': '区块链和P2P网络'}, {'question': '区块链利用____技术解决了账本完整性需求。（  ）',
                                                           'options': ['公开密钥技术', '数字签名和哈希算法',
                                                                       '可拥有多个公钥', 'P2P网络'],
                                                           'correct_answers': '数字签名和哈希算法'}, {
                      'question': '区块的区块头中记录着当前区块的元信息，其中前一区块头Hash保障交易历史的完整性，____保障交易本身的完整性。（ ）',
                      'options': ['区块版本号', '前一区块头Hash', 'Merkle树根Hash', 'Nonce'],
                      'correct_answers': 'Merkle树根Hash'}, {
                      'question': '为了维持区块生成速度，区块链被设计为平均每___分钟生成一个新区块，这需要每隔___个区块定期更新难度值E。（ ）',
                      'options': ['10, 2016', '30, 2016', '10, 1024', '30, 1024'], 'correct_answers': '10, 2016'},
                  {'question': '区块链中运用了什么基础技术来实现隐私保护？（ ）',
                   'options': ['哈希算法', '数字签名', '参与者可拥有多个公钥', '公开密钥技术'],
                   'correct_answers': '参与者可拥有多个公钥'}, {
                      'question': '19世纪荷兰人A.Kerckhoffs就提出了一个在密码学界被公认为基础的假设，也就是著名的“Kerckhoffs假设”：秘密必须全寓于（ ）。',
                      'options': ['密钥', '加密算法', '明文', '密文'], 'correct_answers': '密钥'},
                  {'question': '以下哪个要素不属于对称密钥密码系统？(  )',
                   'options': ['明文', '密文', '密钥', '数字签名'], 'correct_answers': '数字签名'},
                  {'question': '古罗马时代使用的恺撒密码属于(  )。',
                   'options': ['替代密码', '置换密码', '分组密码', '行序列密码'], 'correct_answers': '替代密码'},
                  {'question': 'Vigenère是一种多字母表密码，若被发现（）则很容易遭到攻击。',
                   'options': ['密钥数量', '密钥长度', '字母频率', '偏移量'], 'correct_answers': '密钥长度'},
                  {'question': '下面关于无条件安全和计算安全，说法不正确的是（ ）。',
                   'options': ['假设攻击者有无限的时间，无限的资源，密码都不能被破解称之为无条件安全。',
                               '假设攻击者时间有限计算资源有限的情况下，密码不能被破解称之为计算上安全。', ' ',
                               '如果密钥序列真正随机，且明文序列长度相同，那么该密码无条件安全。'],
                   'correct_answers': 'AES密码是无条件安全的。'}, {'question': '以下古典密码系统中，属于置换密码的是（）。',
                                                                  'options': ['凯撒密码', '羊皮传书', 'PlayFair密码',
                                                                              'Vigenère密码'],
                                                                  'correct_answers': '羊皮传书'},
                  {'question': '相对最容易遭受词频统计分析攻击的是（ ）。',
                   'options': [' ', '单字母表密码', '维吉尼亚密码', ' '], 'correct_answers': '单字母表密码'},
                  {'question': '下面说法不正确的是（ ）。', 'options': ['密码体制包括对称密钥密码和非对称密钥密码两种。',
                                                                     '对称密钥体制中，密钥需要事先由发送方和接收方实现共享。',
                                                                     '有些公开密钥系统中，密钥对互相之间可以交换使用。',
                                                                     '若知道公钥密码的加密算法，从加密密钥得到解密密钥在计算上是可行的。'],
                   'correct_answers': '若知道公钥密码的加密算法，从加密密钥得到解密密钥在计算上是可行的。'},
                  {'question': '信息安全需求包括（ ）。', 'options': ['保密性', '完整性', '抗抵赖性', '以上都是'],
                   'correct_answers': '以上都是'},
                  {'question': '报文的（ ），即验证报文在传送和存储过程中是否被篡改、错序等。',
                   'options': ['保密性', '完整性', '身份认证', '抗抵赖性'], 'correct_answers': '完整性'},
                  {'question': '若发送者使用对称密钥加密报文，则无法实现（ ）。',
                   'options': ['保密性', '完整性', '身份认证', '抗抵赖性'], 'correct_answers': '抗抵赖性'},
                  {'question': '以下哪一项不属于哈希函数的特性（ ）。',
                   'options': ['单向性', '固定长度的输出', '抗碰撞性', '可逆性'], 'correct_answers': '可逆性'},
                  {'question': '对于报文M若找到M’使_____，即找到碰撞能够构成对哈希函数H的攻击。（ ）',
                   'options': ['M=M且H(M’)＝H(M)', 'M’≠M且H(M’) ≠H(M)', 'M’≠M但H(M’)＝H(M)', 'M’=M但H(M’) ≠H(M)'],
                   'correct_answers': 'M’≠M但H(M’)＝H(M)'},
                  {'question': '要找到两个不同的报文x，y，使H(y)=H(x)，在计算上是不可行的。则哈希函数H具有（ ）。',
                   'options': ['单向性', '弱抗碰撞性', '强抗碰撞性', '压缩性'], 'correct_answers': '强抗碰撞性'}, {
                      'question': '发送者用_____对报文签名，然后使用_____加密，同时提供保密性和报文鉴别的所有三种安全服务。（ ）',
                      'options': ['自己的公钥，自己的私钥', '自己的私钥，自己的公钥', '自己的私钥，接收者的公钥',
                                  '自己的公钥，接收者的私钥'], 'correct_answers': '自己的私钥，接收者的公钥'},
                  {'question': '以下不属于Hash算法的是（ ）。', 'options': ['M', 'SH', 'RIPEM', 'RS'],
                   'correct_answers': 'RSA'}, {'question': '发送者使用接收者的公钥加密报文传递给接收者，能实现（ ）。',
                                               'options': ['仅保密', '保密且报文鉴别', '保密与部分报文鉴别',
                                                           '仅报文鉴别'], 'correct_answers': '仅保密'},
                  {'question': '以下的描述中，对报文的数字签名不能实现的是（ ）。',
                   'options': ['保证报文传输过程中的保密性', '保护报文的完整性', '验证报文发送者的身份',
                               '防止报文发送者抵赖'], 'correct_answers': '保证报文传输过程中的保密性'},
                  {'question': '关于UNIX密码文件中的Salt，以下说法不正确的是（ ）。',
                   'options': ['Salt值是随机数', 'Salt可以重复使用', 'Salt可以提高离线字典攻击的穷举空间',
                               '使用Salt，一个口令字符串的hash值最多可以有2^12种不同的输出'],
                   'correct_answers': 'Salt可以重复使用'}, {'question': '以下说法不正确的是（ ）。',
                                                            'options': ['基于口令的认证是弱的认证方法',
                                                                        '动态口令可以完全避免重放攻击',
                                                                        '质询/应答身份认证技术中，质询也可以称为Nonce',
                                                                        '质询/应答身份认证技术中，可以利用对称密钥加密实现双向认证'],
                                                            'correct_answers': '动态口令可以完全避免重放攻击'},
                  {'question': '_____是构造更复杂的交互式认证协议的基本组件。（ ）',
                   'options': ['口令', '质询与应答', 'Needham-Schroeder协议', 'KER'], 'correct_answers': '质询与应答'},
                  {'question': '_____解决了Kerberos协议中的授权问题。（ ）',
                   'options': ['共享的对称密钥', ' ', 'TGS', '数字证书'], 'correct_answers': 'TGS'},
                  {'question': '面哪项是由Needham-Schroeder协议解决的最主要问题？（ ）',
                   'options': ['密钥分发和认证', '保密性和完整性', '认证和完整性', '保密性和可用性'],
                   'correct_answers': '密钥分发和认证'}, {'question': '对于身份认证协议最大的威胁是（ ）。',
                                                          'options': ['穷举攻击', '重放攻击', '字典攻击',
                                                                      '社会工程攻击'], 'correct_answers': '重放攻击'}]

# selenium的配置
service = Service("../MicrosoftWebDriver116.exe")

browser = webdriver.Edge(service=service)

browser.maximize_window()

browser.get("https://www.icourse163.org")

browser.delete_all_cookies()

with open('cookies.txt', 'r') as cookief:
    cookies_list = json.load(cookief)

    for cookie in cookies_list:
        if isinstance(cookie.get('expiry'), float):
            cookie['expiry'] = int(cookie['expiry'])
        browser.add_cookie(cookie)

browser.refresh()
# 加载cookie然后再访问网页，注意cookie的存活时间

# 需要设置等待时间否则会因为待查询网页元素加载不出来报错,只能等待设置一次就行
browser.implicitly_wait(5)


def find_elements_by_Xpath(drive, path):
    try:
        return drive.find_elements(By.XPATH, path)
    except Exception as e:
        # print("查找出错:", e)
        return None


def find_element_by_Xpath(drive, path):
    try:
        return drive.find_element(By.XPATH, path)
    except Exception as e:
        # print("查找出错:", e)
        return None


def wash_str(str1):
    str1 = str1.replace("？", "?")
    str1 = str1.replace("：", ":")
    str1 = str1.replace(" ", "")
    str1 = str1.replace("、", ".")
    return str1


def get_similarity(str1, str2):
    matcher = difflib.SequenceMatcher(None, str1, str2)
    similarity_ratio = matcher.ratio()
    # print(f"Similarity ratio between '{str1}' and '{str2}': {similarity_ratio}")
    return similarity_ratio

    # {'question': 'PKI通过引入____解决如何相信公钥与身份的绑定关系的问题。',
    #  'options': ['密钥共享', 'SET协议', '证书', '数字签名'],
    #  'correct_answers': '证书'}


# 重新打开网页就进入到了选择单元测试界面
browser.get("https://www.icourse163.org/learn/FUDAN-1206357811?tid=1471259447&learnMode=0#/learn/quiz?id=1244091799")

# 查找各个题目部分
sections = find_elements_by_Xpath(browser,
                                  '//*[@id="courseLearn-inner-box"]/div/div[3]/div/div[4]/div/div[1]/div[1]/div')
# 框架找到
if sections is not None:
    for section in sections:
        time.sleep(0.5)
        # 抽取具体题目text
        question_text = find_element_by_Xpath(section, './/div[1]/div[2]/div[3]/p').text
        # 题库搜搜题目、特殊考虑存在相同用题目而且只有单选题
        if question_text is not None:
            re = True
            for Q in questions_json:
                if get_similarity(Q.get('question'), question_text) > 0.85:
                    print(Q.get('question'))
                    # 成功找到题目之后查找正确答案，然后选择选项
                    # 题目的对应选项
                    answers = find_elements_by_Xpath(section, './/div[2]/ul/li')
                    if answers is not None:
                        max_similarity=0.8
                        for answer in answers:
                            # 获取选项文本
                            time.sleep(0.5)
                            answer_click = find_element_by_Xpath(answer, './/label/div[2]/p')
                            answer_text = answer_click.text
                            # print("答案相似度:", answer_text, get_similarity(answer_text, Q.get('correct_answers')))
                            if get_similarity(answer_text, Q.get('correct_answers')) >= max_similarity:
                                max_similarity=get_similarity(answer_text, Q.get('correct_answers'))
                                print("选择答案:", answer_text, get_similarity(answer_text, Q.get('correct_answers')))
                                answer_click.click()
                        print("正确答案:", Q.get('correct_answers'))
                        print('-' * 20)
                        re = False
                        continue
                    else:
                        print('答案选项为空')
            if re:
                print('匹配失败:', question_text)
        else:
            print('未找到题目')


else:
    print("题目框找不到")

print("题目填写结束进行检查")
# 检查并且提交答案
time.sleep(100)
# 不论是否成功，最终都关闭browser
browser.quit()
