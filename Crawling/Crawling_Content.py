from datetime import date, timedelta
from selenium import webdriver
from bs4 import BeautifulSoup
from multiprocessing import Process
import time
import requests
import re
import csv
import datetime

def delete(url_count, news_press, news_category, news_headline, news_url, news_date):
    del news_press[url_count]
    del news_category[url_count]
    del news_headline[url_count]
    del news_url[url_count]
    del news_date[url_count]
    return news_press, news_category, news_headline, news_url, news_date

def preprocess(text):
    text = re.sub('<.+?>|&nbsp;|br|⊙|※|▲|◆|▶|■|●|○|△|□|  ', '', str(text))
    text = text.replace("\n", "")
    text = text.replace("\r", "")
    text = text.strip()
    return text

def crawl_news_text(news_press, news_category, news_headline, news_url, news_date):  # 긁어온 url들 들어가서 뉴스 본문 긁기
    fail_count = 0  # url에 본문 내용이 없을 때 count
    news_main_text = []

    # print('press : ' + news_press[0])
    # print('category : ' + news_category[0])
    # print('headline : ' + news_headline[0])
    # print('url : ' + news_url[0])
    # print('date : ' + news_date[0])
    for url_count in range(0, len(news_url)): # 빅카인즈에서 긁어온 url 수만큼 반
        time.sleep(1)
        url_html = requests.get(news_url[url_count - fail_count]).content
        soup = BeautifulSoup(url_html, 'html.parser')
        #print(self.news_url[url_count - fail_count])
        # 각 기사의 언론사에 맞게 크롤
        #if '경향신문' in self.news_press[url_count]:
        #    self.news_main_text.append(self.preprocess(soup.select_one('#articleBody').get_text()))
        if '국민일보' in news_press[url_count - fail_count]:
            tag = soup.select_one('#articleBody')
            if tag == None:    # url에 본문 내용 없을 때
                news_press, news_category, news_headline, news_url, news_date = delete(url_count - fail_count, news_press, news_category, news_headline, news_url, news_date) # 모든 list에서 해당 url에 대한 정보 삭제
                fail_count += 1
            else:
                news_main_text.append(preprocess(tag.text))
        elif '내일신문' in news_press[url_count - fail_count]:
            tag = soup.select_one('#contents > p')
            if tag == None:
                news_press, news_category, news_headline, news_url, news_date = delete(url_count - fail_count, news_press, news_category, news_headline, news_url, news_date)
                fail_count += 1
            else:
                news_main_text.append(preprocess(tag.text))
        elif '동아일보' in news_press[url_count - fail_count]:
            tag = soup.select_one('#content > div > div.article_txt')
            if tag == None:
                news_press, news_category, news_headline, news_url, news_date = delete(url_count - fail_count, news_press, news_category, news_headline, news_url, news_date)
                fail_count += 1
            else:
                for span in tag.select('span'):
                    span.decompose()
                for ul in tag.select('ul'):
                    ul.decompose()
                for strong in tag.select('strong'):
                    strong.decompose()
                for a in tag.select('a'):
                    a.decompose()
                news_main_text.append(preprocess(tag.text))
        elif '문화일보' in news_press[url_count - fail_count]:
            tag = soup.select_one('#NewsAdContent')
            if  tag == None:
                news_press, news_category, news_headline, news_url, news_date = delete(url_count - fail_count, news_press, news_category, news_headline, news_url, news_date)
                fail_count += 1
            else:
                news_main_text.append(preprocess(tag.text))
        elif '서울신문' in news_press[url_count - fail_count]:
            if 'go' in news_url[url_count - fail_count]:
                tag = soup.select_one('#article_content')
                if tag == None:
                    news_press, news_category, news_headline, news_url, news_date = delete(url_count - fail_count, news_press, news_category, news_headline, news_url, news_date)
                    fail_count += 1
                else:
                    news_main_text.append(preprocess(tag.text))
            elif 'now' in news_url[url_count - fail_count]:
                tag = soup.select_one('#articleContent')
                if tag == None:
                    news_press, news_category, news_headline, news_url, news_date = delete(url_count - fail_count, news_press, news_category, news_headline, news_url, news_date)
                    fail_count += 1
                else:
                    news_main_text.append(preprocess(tag.text))
            elif 'stv' in news_url[url_count - fail_count]:
                tag = soup.select_one('#CmAdContent')
                if tag == None:
                    news_press, news_category, news_headline, news_url, news_date = delete(url_count - fail_count, news_press, news_category, news_headline, news_url, news_date)
                    fail_count += 1
                else:
                    news_main_text.append(preprocess(tag.text))
            elif 'biz' in soup.select_one('link').get('href'):
                tag = soup.select_one('body > div > div.middleWrap > div > div.mLeftWrap > div.articleDiv')
                if tag == None:
                    news_press, news_category, news_headline, news_url, news_date = delete(url_count - fail_count, news_press, news_category, news_headline, news_url, news_date)
                    fail_count += 1
                else:
                    news_main_text.append(preprocess(tag.text))
            else:
                tag = soup.select_one('#atic_txt1')
                if tag == None:
                    news_press, news_category, news_headline, news_url, news_date = delete(url_count - fail_count, news_press, news_category, news_headline, news_url, news_date)
                    fail_count += 1
                else:
                    for table in tag.select('table'):
                        table.decompose()
                    for div in tag.select('div'):
                        div.decompose()
                    news_main_text.append(preprocess(tag.text))                
        elif '세계일보' in news_press[url_count - fail_count]:
            tag = soup.select_one('#article_txt > article')
            if tag == None:
                    news_press, news_category, news_headline, news_url, news_date = delete(url_count - fail_count, news_press, news_category, news_headline, news_url, news_date)
                    fail_count += 1
            else:
                for figure in tag.select('figure'):
                    figure.decompose()
                news_main_text.append(preprocess(tag.text))
        #elif '조선일보' in news_press[url_count - fail_count]:
        #    news_main_text.append(preprocess(soup.select_one('#articleBody').get_text()))
        elif '중앙일보' in news_press[url_count - fail_count]:
            tag = soup.select_one('#article_body')
            if tag == None:
                    news_press, news_category, news_headline, news_url, news_date = delete(url_count - fail_count, news_press, news_category, news_headline, news_url, news_date)
                    fail_count += 1
            else:
                for div in tag.select('div'):
                    div.decompose()
                news_main_text.append(preprocess(tag.text))
        elif '한겨레' in news_press[url_count - fail_count]:
            tag = soup.select_one('div.article-text > div > div.text')
            if tag == None:
                news_press, news_category, news_headline, news_url, news_date = delete(url_count - fail_count, news_press, news_category, news_headline, news_url, news_date)
                fail_count += 1
            else :
                for div in tag.select('div'):
                    div.decompose()
                news_main_text.append(preprocess(tag.text))
        elif '한국일보' in news_press[url_count - fail_count]:
            tag = soup.select_one('body > div.wrap > div.container.end > div > div > div > p')
            if tag  == None:
                    news_press, news_category, news_headline, news_url, news_date = delete(url_count - fail_count, news_press, news_category, news_headline, news_url, news_date)
                    fail_count += 1
            else:
                text = ""
                result_set = soup.select('body > div.wrap > div.container.end > div > div > div > p')
                for p in result_set:
                    text = text + p.text   
                news_main_text.append(preprocess(text).replace('user@hankookilbo.com보내는 기사', ''))
    return news_press, news_category, news_headline, news_url, news_date, news_main_text

def save_data(id, filename, news_press, news_category, news_headline, news_url, news_date, news_main_text):    # 크롤한 정보들 CSV로 저장
    file = open(str(id) + "_" + filename, 'w', encoding='utf-8', newline = '')
    writer = csv.writer(file)
    writer.writerow(["date", "press", "category", "headline", "url", "text"])
    for l in range(0, len(news_url)):
        writer.writerow([news_date[l], news_press[l], news_category[l], news_headline[l], news_url[l], news_main_text[l]])
        
    file.close()

def work(id, filename, news_press, news_category, news_headline, news_url, news_date):
    start = datetime.datetime.now()

    news_press, news_category, news_headline, news_url, news_date, news_main_text = crawl_news_text(news_press, news_category, news_headline, news_url, news_date)
    save_data(id, filename, news_press, news_category, news_headline, news_url, news_date, news_main_text)
    
    finish = datetime.datetime.now()
    print(id, finish - start)
if __name__ == "__main__":
    filename = "201909.csv"
    news_press = []
    news_category = []
    news_headline = []
    news_url = []
    news_main_text = []
    news_date = []

    f = open(filename, "r", encoding='utf-8')
    rdr = csv.reader(f)
    for row in rdr:
        news_press.append(row[0])
        news_category.append(row[1])
        news_headline.append(row[2])
        news_url.append(row[3])
        news_date.append(row[4])

    news_press, news_category, news_headline, news_url, news_date = delete(0, news_press, news_category, news_headline, news_url, news_date)
    press_list = []
    category_list = []
    headline_list = []
    url_list = []
    date_list = []
    
    j = 0
    process_count = 0
    print('news amount : ' + str(len(news_press)))
    for i in range(0, len(news_press), 1):
        press_list.append(news_press[i])
        category_list.append(news_category[i])
        headline_list.append(news_headline[i])
        url_list.append(news_url[i])
        date_list.append(news_date[i])
        j = j + 1
        if(j == 5000):
            print('divide!!')
            process_count = process_count + 1
            if process_count == 5:
                p = Process(target = work, args = (process_count, filename, press_list, category_list, headline_list, url_list, date_list))
                p.start()
            press_list.clear()
            category_list.clear()
            headline_list.clear()
            url_list.clear()
            date_list.clear()
            j = 0
        if(i == len(news_press) - 1):
            print('divide!!')
            process_count = process_count + 1
            # if process_count == 5:
            # p = Process(target = work, args = (process_count, filename, press_list, category_list, headline_list, url_list, date_list))
            # p.start()
            press_list.clear()
            category_list.clear()
            headline_list.clear()
            url_list.clear()
            date_list.clear()
            break
