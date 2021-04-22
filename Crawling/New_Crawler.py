from multiprocessing import Process
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime
import time
import re

def preprocess(text):
    text = re.sub('<.+?>|&nbsp;|br|⊙|※|▲|◆|▶|■|○|△|□|-|<|>|…|\n|\r|\t|\xa0|  ', '', str(text))
    text = re.sub('([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,})', '', text)
    text = text.strip()
    return text
    
def getRequestUrl(url):   
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            return response
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None
    
def savedata(id, filename, result):
    tbl = pd.DataFrame(result, columns = ('date', 'press', 'category', 'headline', 'url', 'text', 'img'))
    tbl.to_csv(str(id) + "_" + filename, encoding = 'utf-8-sig', mode = 'w', index = False)
    del result[:]
        
def crawler(result, news_date, news_press, news_category, news_headline, news_url):
    for url_count  in range(0, len(news_url)):
        #time.sleep(1)
        
        html = getRequestUrl(news_url[url_count])
        if html == None:
            continue
        soup = BeautifulSoup(html, 'html.parser')
        if soup == None:
            continue
        
        news_text = []
        news_img = []
        if '국민일보' in news_press[url_count]:
            tag = soup.select_one("#articleBody")
            if tag == None:
                continue
            if tag.select_one("img") != None:
                news_img = tag.select_one("img").get("src")
            for div in tag.select("div"):
                div.decompose()
            tmp = preprocess(tag.text)
            news_text = tmp.replace('GoodNews paper ⓒ 국민일보(www.kmib.co.kr), 무단전재 및 수집, 재배포금지', '')
        elif '내일신문' in news_press[url_count]:
            tag = soup.select_one("#contents")
            if tag == None:
                continue
            if tag.select_one("img") != None:
                news_img = tag.select_one("img").get("src")
            news_text = preprocess(tag.text)
        elif '동아일보' in news_press[url_count]:
            tag = soup.select_one("#content > div > div.article_txt")
            if tag == None:
                continue
            if tag.select_one("img") != None:
                news_img = tag.img.get("src")
            for div in tag.select("div"):
                div.decompose()
            news_text = preprocess(tag.text)
        elif '문화일보' in news_press[url_count]:
            tag = soup.select_one("#NewsAdContent")
            if tag == None:
                continue
            if tag.select_one("img") != None:
                news_img = tag.img.get("src")
            for b in tag.select("b"): # 중간글 삭제
                b.decompose()
            news_text = preprocess(tag.text)
        elif '서울신문' in news_press[url_count]:
            # go
            if "go" in news_url[url_count]:
                tag = soup.select_one("#article_content")
                if tag == None:
                    continue
                if tag.select_one("img") != None:
                    news_img = tag.img.get("src")
                for div in tag.select("div"):# 끝에 필요없는 정보 제거
                    div.decompose()
                news_text = preprocess(tag.text)
            else:
                #일반
                tag = soup.select_one("#atic_txt1")
                if tag == None:
                    continue
                if tag.select_one("img") != None:
                    news_img = tag.img.get("src")
                for span in tag.select("span"): # 사진 출처 제거
                    span.decompose()
                news_text = preprocess(tag.text)
        elif '세계일보' in news_press[url_count]:
            tag = soup.select_one("#article_txt")
            if tag == None:
                continue
            if tag.select_one("img") != None:
                news_img = tag.img.get("src")
            for figcaption in tag.select("figcaption"): # 사진 출처 제거
                figcaption.decompose()
            tmp = preprocess(tag.text)
            news_text = tmp.replace("[ⓒ 세계일보 & Segye.com, 무단전재 및 재배포 금지]", "")
        elif '중앙일보' in news_press[url_count]:
            tag = soup.select_one("#article_body")
            if tag == None:
                continue
            if tag.select_one("img") != None:
                news_img = tag.img.get("src")
            for div in tag.select("div"):
                div.decompose()
            news_text = preprocess(tag.text)
        elif '한겨레' in news_press[url_count]:
            tag = soup.select_one("#a-left-scroll-in > div.article-text")
            if tag == None:
                continue
            if tag.select_one("img") != None:
                news_img = tag.img.get("src")
            tag = tag.select_one("div.text")
            if tag == None:
                continue
            for div in tag.select("div"):
                div.decompose()
            news_text = preprocess(tag.text)
        
        result.append([news_date[url_count]] + [news_press[url_count]] + [news_category[url_count]] + [news_headline[url_count]] + [news_url[url_count]] + [news_text] + [news_img])
            
def work(id, filename, news_date, news_press, news_category, news_headline, news_url):
    start = datetime.datetime.now()
    
    result = []
    crawler(result, news_date, news_press, news_category, news_headline, news_url)
    savedata(id, filename, result)
    
    finish = datetime.datetime.now()
    print(str(id) + "process finished", finish - start)
        
if __name__ == "__main__":
    filename = "202001.csv"
    
    # 파일 읽어들이기
    df = pd.read_csv(filename, encoding="utf-8-sig")
    news_date = df['date'].tolist()
    news_press = df['press'].tolist()
    news_category = df['category'].tolist()
    news_headline = df['headline'].tolist()
    news_url = df['url'].tolist()
    
    date_list = []
    press_list = []
    category_list = []
    headline_list = []
    url_list = []
    
    print('news amount : ' + str(len(news_press)))
    
    news_count = 0
    process_count = 0
    for i in range(0, len(news_press), 1):
        date_list.append(news_date[i])
        press_list.append(news_press[i])
        category_list.append(news_category[i])
        headline_list.append(news_headline[i])
        url_list.append(news_url[i])
        
        news_count = news_count + 1
        if(news_count == 5000):
            print('divide!!')
            process_count = process_count + 1
            #if process_count == 5:
            p = Process(target = work, args = (process_count, filename, date_list, press_list, category_list, headline_list, url_list))
            p.start()
            date_list.clear()
            press_list.clear()
            category_list.clear()
            headline_list.clear()
            url_list.clear()
            
            news_count = 0
            
        if(i == len(news_press) - 1):
            print('divide!!')
            process_count = process_count + 1
            p = Process(target = work, args = (process_count, filename, date_list, press_list, category_list, headline_list, url_list))
            p.start()
            
            date_list.clear()
            press_list.clear()
            category_list.clear()
            headline_list.clear()
            url_list.clear()
            
            break