import requests
from bs4 import BeautifulSoup
# 获取所有超链接地址
# 首先，我们需要找到所有的超链接标签
# 然后，我们需要从每个标签中提取出 href 属性的值
# 最后，我们将所有的 href 值写入到一个文件中

url = 'https://cesium.com/learn/cesiumjs/ref-doc/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a')

# 如果href不包含host, 则自动加上host
for link in links:
    href = link.get('href')
    if href and not href.startswith('http'):
        link['href'] = url + href


# 只保留包含/ref-doc/的href
links = [link for link in links if '/ref-doc/' in link.get('href')]


# with open('Cesium106文档链接们.txt', 'w') as f:
#     for link in links:
#         f.write(link.get('href') + '\n')

output = ''
for i, link in enumerate(links[292:]):
    href = link.get('href')
    response = requests.get(href)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()

    text = ' '.join(text.split())

    text = text.replace('\u2192', '->')
    text = text.replace('\n', ' ').replace('\r', '')
    text = ' '.join(text.split())
    index = text.find("Need help?")
    if index != -1:
        text = text[:index]

    text = "\n".join([line for line in text.split("\n") if line.strip() != ""])

    name = href.split('/')[-1]
    text += '\n\n' + name + '\n\n'

    output += text
    index = href.rfind('/')

    print(name, len(output))
    print(f"{i+1+292}/{len(links)}")


    with open('output.txt', 'a') as f:
        f.write(text.encode('utf-8').decode('gbk', 'ignore'))
