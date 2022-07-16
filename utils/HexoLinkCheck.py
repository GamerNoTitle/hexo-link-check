from flask import Blueprint, request
import requests
from lxml import etree
import re
from urllib import parse
import _thread

blueprint = Blueprint('hexo_link_check', __name__,
                      url_prefix='/hexo_link_check')


def StartCheck(url):
    try:
        _thread.start_new_thread(get_link, (url,))
        return {'code': 0, 'msg': '检查请求提交成功！请等待约两分钟（可能更久）后在报告查看页面进行查看！'}
    except Exception as e:
        return {'code': -1, 'msg': f'请求提交失败，得到了 {e} 错误！'}


def get_link(url, ss=False):
    """
    检查自己的友链状态
    :param url: 输入自己的博客友链
    :param ss: 是从自己的博客友链获取还是自己添加去查询对方是否添加了自己，默认从自己博客获取
    :return:
    """
    print(f'Start checking {url}')
    filename = 'hexo-link-check/' + url.replace('http://', '').replace('https://',
                                                                       '').replace('/link', '').replace('/', '')
    file = open(filename, 'wt+', encoding='utf8')
    if 'https://' not in url and 'http://' not in url:  # 缺少协议头时自动补齐
        url = 'http://' + url
    file.write(f'正在开始对 {url} 发起检查……\n')
    # 发现有些博客有检查user-agent，所以加上这个
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/75.0.3770.142 Safari/537.36'}
    if ss is False:

        ret = requests.get(url, headers=header).content.decode('utf8')
        # print(ret)
        soup = etree.HTML(ret)
        # //*[@id="article-container"]/div/div[2]/div[1]/a
        # //*[@id="article-container"]/div/div[4]/div[1]/a/div[2]title cf-friends-name
        # //*[@id="article-container"]/div/div[1]/div[1]/a[1]/div[2]/span[1]
        friend_url = soup.xpath('//*[@id="article-container"]//@href')
        # friend_name = soup.xpath('//*[@id="article-container"]//div/a/div[@class="flink-item-name"]/text()')
        # 名字位置都不一样 就不判断了
        # friend_name = soup.xpath('//*[@id="article-container"]//span[@class="title"]/text()')
        # print(friend_name)
        urls = re.findall(
            r'(?:http.?|ftp|file)://[-A-Za-z\d+&@#/%?=~_|!:,.;]+[-A-Za-z\d+&@#/%=~_|]', str(friend_url))
        if not urls:
            return "支持Butterfly主题，不魔改友链的；可能支持部分Hexo主题。但是既然弹了这个提示就说明不支持啦~"
    else:
        urls = ['想查对方是否有你在这输入对方的友链地址1', '想查对方是否有你在这输入对方的友链地址2']

    n = len(urls)
    x = 0
    d = 0
    d1 = 0
    d2 = 0

    success = ''
    none = ''
    error = ''
    import urllib3
    urllib3.disable_warnings()
    file.write("检查开始了，你一共有 %s 个友链\n" % n)
    for i in urls:
        x += 1
        friend_url = i
        url1 = parse.urlparse(url).netloc
        url2 = url1.split('.')
        url3 = url1 if len(url2) < 3 else url2[1] + "." + url2[2]
        if url3 in friend_url:
            file.write((friend_url + f"：第 {str(x)} 个，自己就不检查了撒\n"))
        else:
            if ss is False:
                # 自己输入就不用加/link路径了
                if friend_url[len(friend_url) - 1:] == '/':
                    friend_url += 'link/'
                else:
                    friend_url += '/link/'
            # if 'https' in friend_url:
            #     friend_url = 'http' + friend_url[5:]
            try:
                ret = requests.get(friend_url, headers=header,
                                   verify=False, timeout=60)
            except requests.exceptions.ConnectionError as e:
                file.write(f'访问 {friend_url} 时出现了错误: {e}\n')
            if not ret.status_code == 200:
                d += 1
                error += friend_url + '\n'
                file.write((f"第 {str(x)} 个，{friend_url} 链接有误，可能友链不是link，进度：" +
                            str(round(x / n * 100, 1)) + "%") + '\n')
            else:
                # soup = etree.HTML(ret.text)
                # ffriend_url = soup.xpath('//*[@id="article-container"]//@href')
                if url1 in str(ret.text):
                    d1 += 1
                    success += friend_url + '\n'
                    file.write((f"第 {str(x)} 个，{friend_url} 添加我了，进度：" + str(round(x /
                                                                                  n * 100, 1)) + "%") + '\n')
                else:
                    d2 += 1
                    none += friend_url + '\n'
                    file.write((f"第 {str(x)} 个，{friend_url} 没有添加我，进度：" + str(round(x /
                                                                                   n * 100, 1)) + "%") + '\n')
    file.write('统计结果：\n链接有误的有%s个，其中添加了我的有%s个，没有添加我的有%s个\n' % (str(d), str(d1), str(
        d2)) + '添加了我的：\n' + success + '未添加我的：\n' + none + '链接可能存在错误的：\n' + error)
    file.close()
    file = open(filename, 'r', encoding='utf8')
    result = file.read()
    file.close()
    return result


def get_str_btw(s, f, b):
    par = s.partition(f)
    return (par[2].partition(b))[0][:]


if __name__ == '__main__':
    # 输入待检查的博客友链地址即可
    url = 'https://bili33.top/link/'
    get_link(url)
