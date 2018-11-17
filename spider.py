import re
import requests
from bs4 import BeautifulSoup


def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def getStockList(lst, stockURL):
    # 获得一个页面
    html = getHTMLText(stockURL)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            lst.append(re.findall(r"[s][hz]\d{6}", href)[0])
        except:
            continue


def getStockInfo(lst, stockURL, fpath):
    count = 0
    for stock in lst:
        url = stockURL + stock + ".html"
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            infoDict = {}
            soup = BeautifulSoup(html, 'html.parser')
            stockInfo = soup.find('div', attrs={'class': 'stock-bets'})

            name = stockInfo.find_all(attrs={'class': 'bets-name'})[0]
            # split()的意思是股票名称空格后面的部分不需要了
            infoDict.update({'股票名称': name.text.split()[0]})

            keyList = stockInfo.find_all('dt')
            valueList = stockInfo.find_all('dd')

            # 获得的键和值按键值对的方式放入字典
            for i in range(len(keyList)):
                key = keyList[i].text
                val = valueList[i].text
                infoDict[key] = val

            # 把字典中的数据存入外部文件
            with open(fpath, 'a', encoding='utf-8')as f:
                f.write(str(infoDict) + '\n')
                count += 1
                print("\r当前进度:{:.2f}%".format(count * 100 / len(lst)), end="")
        except:
            count += 1
            print("\r当前进度:{:.2f}%".format(count * 100 / len(lst)), end="")
            continue


def main():
    # 一只股票信息的网址
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    # 百度股票网的网址
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    output_fist = 'BaiduStockInfo.txt'
    slist = []
    getStockList(slist, stock_list_url)
    getStockInfo(slist, stock_info_url, output_fist)


if __name__ == '__main__':
    main()
