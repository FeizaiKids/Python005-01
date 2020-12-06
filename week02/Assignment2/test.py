import requests
from lxml import etree
from time import sleep
from pathlib import *
import sys

def get_url_name(myurl):
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'

    header = {
        'user-agent':ua,
        'Referer' : 'https://www.zhihu.com/signin?next=%2F'
        }
    
    s = requests.Session()
    login_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
    form_data = 'aR79k4U0cT2tXqYq8LPG6vHmxq2pkLnmtbSBDgg9kLtxgeSmhbfGiqX1jbfVoG398LF0gQN0cT2tuqYq8LkMQbwGivwOgUxGw9e0g4e8kCV92vgBzh3qk4R92LkYFhVGwqoVJbCGST2tEqx9BLkBEJXmST2tXGYq8LP9c4U0g_epcTYhBT2_k4U0gXFXoL2qmLt02iu0QRFXE8Y0mTLqc79hth2pkLP9sLF0gQU0th2pkLn0m72qce90cRYxQRt017FZbAU_cLtxgTLqsTYhug9qkLPxkLF0z0pGEqemQvgVcu3mthF0c79hth2pkLP9sLF0g6uqth2pkLP01TF_c4U0gXLxcTYh8TYqk4_BjgOOsGOmthF0c79hPG2pkLP9BLf8igXGQwOfSTYhY7YqS7UqNgVOXqYhyhomogcMUuppkLfmwqNZAqL8JGNxeLF0zAOGEeHm-qpuDCNBtgp924_BJwx9kCSMsBF0g6e0o8SxUwF0GLx0Ug90272p6LF88R2qgrUBgUYfrXOys0F8b7r0gqFm2LfB8CpGU9eBDqppkLn8zG3ZchL1iDpuJvS8EqYhggHMcvOOSTYhs0ty2HU0Q8txoRFqm_e0giCmU9VOgcO1KBF0g6HM-GVO2wxMEqYhgDCKevgVEwNMqBF0giU0gutpr0YBmXNqgq982TNXNqtqfXY8SQr8o8SYFq28EqYhHqeVebSYDrS8: '

    # post数据前获取cookie
    pre_login = 'https://www.zhihu.com/api/v3/oauth/sign_in'
    pre_resp = s.get(pre_login, headers = header)
    
    response = s.post(login_url, data=form_data, headers=header, cookies=s.cookies)
    
    try:
        response = requests.get(myurl, headers=header, cookies=s.cookies)
    except requests.exceptions.ConnectTimeout as e :
        print(f"requests库超时")
        sys.exit(1)
    
    selector = etree.HTML(response.text)

    answer_name = selector.xpath('//div[@class="ContentItem ArticleItem"]/h2/a/text()')
    answer_link = selector.xpath('//div[@class="ContentItem ArticleItem"]/h2/a/@href')
        
    answer_info = dict(zip(answer_name, answer_link))


    
    p = Path(__file__)
    pyfile_path = p.resolve().parent

    html_path= pyfile_path.joinpath('result')

    if not html_path.is_dir():
        Path.mkdir(html_path)
    page = html_path.joinpath('result.txt')

    # 上下文管理器
    try:
        with open(page, 'w',  encoding='utf-8') as f:            
            for i in answer_info:                
                f.write(f'答案名称： {i} \t\t 答案链接： {answer_info[i]} \n')
    except FileNotFoundError as e:
        print(f'文件无法打开,{e}')
    except IOError as e:
        print(f'读写文件出错,{e}')
    except Exception as e:
        print(e)

if __name__ == '__main__':        
    urls = 'https://www.zhihu.com/topic/20518489/hot'   
    get_url_name(urls)