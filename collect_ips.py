import requests
from bs4 import BeautifulSoup
import re
import os
import time # Import time for potential delays

# 目标URL列表
urls = [
    'https://monitor.gacjie.cn/page/cloudflare/ipv4.html',
    'https://ip.164746.xyz',
    'https://ipdb.030101.xyz/bestcfv4/'
]

# 正则表达式用于匹配IP地址
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 存储找到的唯一IP地址的集合
found_ips = set()

# 检查ip.txt文件是否存在,如果存在则删除它
if os.path.exists('ip.txt'):
    try:
        os.remove('ip.txt')
        print("已删除现有的 ip.txt 文件。")
    except OSError as e:
        print(f"删除 ip.txt 文件时发生错误: {e}")
        # 如果删除失败，可以选择退出或继续，这里选择继续并覆盖写入

# 创建一个文件来存储IP地址
# 使用 'a' 模式以便在删除失败时可以继续写入
try:
    with open('ip.txt', 'w', encoding='utf-8') as file: # Use 'w' mode to overwrite, and specify encoding
        for url in urls:
            print(f"正在处理 URL: {url}")
            try:
                # 发送HTTP请求获取网页内容，设置超时和User-Agent
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(url, headers=headers, timeout=10) # Set a timeout of 10 seconds
                response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

                # 使用BeautifulSoup解析HTML
                soup = BeautifulSoup(response.text, 'html.parser')

                # 根据网站的不同结构找到包含IP地址的元素
                elements = []
                if url == 'https://monitor.gacjie.cn/page/cloudflare/ipv4.html':
                    elements = soup.find_all('tr')
                elif url == 'https://ip.164746.xyz':
                    elements = soup.find_all('tr')
                elif url == 'https://ipdb.030101.xyz/bestcfv4/':
                    elements = soup.find_all('li')
                else:
                    print(f"未知 URL 结构，跳过: {url}")
                    continue # Skip to the next URL if structure is unknown

                if not elements:
                    print(f"在 {url} 中未找到指定的元素。")

                # 遍历所有元素,查找IP地址
                for element in elements:
                    element_text = element.get_text()
                    ip_matches = re.findall(ip_pattern, element_text)

                    # 如果找到IP地址，添加到集合中
                    for ip in ip_matches:
                        found_ips.add(ip)

            except requests.exceptions.RequestException as e:
                print(f"请求 URL 时发生错误 {url}: {e}")
            except Exception as e:
                print(f"处理 URL {url} 时发生未知错误: {e}")

            # Optional: Add a small delay between requests to be polite
            # time.sleep(1)

        # 将集合中的唯一IP地址写入文件
        if found_ips:
            for ip in found_ips:
                file.write(ip + '\n')
            print(f'已将 {len(found_ips)} 个唯一IP地址保存到 ip.txt 文件中。')
        else:
            print("未找到任何IP地址。")

except IOError as e:
    print(f"写入 ip.txt 文件时发生错误: {e}")

print('脚本执行完毕。')

