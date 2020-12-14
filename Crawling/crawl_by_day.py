from datetime import date, timedelta
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import re
import csv

from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def date_calculate(temp_start, temp_end):
    date_list = []
    start_date = date(int(temp_start[0:4]), int(temp_start[4:6]), int(temp_start[6:]))
    end_date = date(int(temp_end[0:4]), int(temp_end[4:6]), int(temp_end[6:]))
    days = end_date - start_date + timedelta(days=1)

    for i in range(days.days):
        date_list.append(start_date + timedelta(days=i))
    return date_list
        
class Big_Kinds_Crawler(object):
    def __init__(self):
        self.news_press = [] # 언론사
        self.news_category = [] # 뉴스 카테고리
        self.news_headline = [] # 뉴스 헤드라인
        self.news_url = []  # 뉴스 url
        self.news_main_text = []    # 뉴스 본문
        self.news_date = []  # 뉴스 날짜
        self.date_list = []  # 기간 내 날짜들

    @staticmethod
    def preprocess(text):
        text = re.sub('<.+?>|&nbsp;|br|⊙|※|▲|◆|▶|■|●|○|△|□|  ', '', str(text))
        text = text.replace("\n", "")
        text = text.replace("\r", "")
        text = text.strip()
        return text

    def delete(self, url_count):
        del self.news_press[url_count]
        del self.news_category[url_count]
        del self.news_headline[url_count]
        del self.news_url[url_count]
        del self.news_date[url_count]

    def crawl_news_url(self, start, end):   # 빅카인즈에서 뉴스별 url, 언론사, 헤드라인, 날짜, 카테고리 크롤

        driver = webdriver.Chrome('/Users/manda/OneDrive/바탕 화면/Utilities/chromedriver_win32/chromedriver')
        driver.implicitly_wait(3)
        driver.get('https://www.bigkinds.or.kr/')

        driver.implicitly_wait(1)

        # 팝업 창 닫기
        html_popup = driver.page_source
        soup_popup = BeautifulSoup(html_popup, 'html.parser')
        if soup_popup.select('#contents > div.popup-container') != None:
            driver.find_element_by_css_selector('div.popup-footer > div > div > button').click()
            
        # 기간 설정
        driver.find_element_by_id('date-filter-btn').click()    # 기간 버튼
        #driver.find_element_by_css_selector('#date-filter-div > div > div:nth-child(1) > button:nth-child(1)').click() # 1일 버튼
        #driver.find_element_by_css_selector('#date-filter-div > div > div:nth-child(1) > button:nth-child(2)').click() # 1주 버튼
        #driver.find_element_by_css_selector('#date-filter-div > div > div:nth-child(1) > button:nth-child(3)').click() # 1개월 버튼
        #driver.find_element_by_css_selector('#date-filter-div > div > div:nth-child(1) > button:nth-child(4)').click() # 3개월 버튼
        #driver.find_element_by_css_selector('#date-filter-div > div > div:nth-child(1) > button:nth-child(5)').click() # 6개월 버튼
        #driver.find_element_by_css_selector('#date-filter-div > div > div:nth-child(1) > button:nth-child(6)').click() # 1년 버튼
        driver.find_element_by_id('search-begin-date').send_keys('\b\b\b\b\b\b\b\b\b\b' + str(start.year) + '-' + str(start.month) + '-' + str(start.day)) # 시작 날짜 입력
        driver.find_element_by_id('search-end-date').send_keys('\b\b\b\b\b\b\b\b\b\b' + str(end.year) + '-' + str(end.month) + '-' + str(end.day))   # 끝 날짜 입력
        driver.find_element_by_id('date-confirm-btn').click()   # 기간 적용 버튼

        # 언론사 설정
        driver.find_element_by_id('provider-filter-btn').click()    # 언론사 버튼  
        #driver.find_element_by_id('중앙지').click()    # 중앙지 체크박스
        #driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(1) > div > button:nth-child(1)').click()    # 경향
        driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(2)').click()    # 국민
        driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(3)').click()    # 내일
        driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(4)').click()    # 동아
        driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(5)').click()    # 문화
        driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(6)').click()    # 서울
        driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(7)').click()    # 세계
        #driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(8)').click()    # 조선
        driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(9)').click()    # 중앙
        driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(10)').click()   # 한겨레
        #driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(11)').click()   # 한국

        driver.implicitly_wait(1)

        # 카테고리 설정
        driver.find_element_by_id('category-filter-btn').click()    # 카테고리 버튼
        driver.find_element_by_css_selector('#category-tree-wrap > ul > li:nth-child(1) > div > span:nth-child(3)').click() # 정치
        driver.find_element_by_css_selector('#category-tree-wrap > ul > li:nth-child(2) > div > span:nth-child(3)').click() # 경제
        driver.find_element_by_css_selector('#category-tree-wrap > ul > li:nth-child(3) > div > span:nth-child(3)').click() # 사회
        #driver.find_element_by_css_selector('#category-tree-wrap > ul > li:nth-child(4) > div > span:nth-child(3)').click() # 문화
        driver.find_element_by_css_selector('#category-tree-wrap > ul > li:nth-child(5) > div > span:nth-child(3)').click() # 국제
        #driver.find_element_by_css_selector('#category-tree-wrap > ul > li:nth-child(6) > div > span:nth-child(3)').click() # 지역
        #driver.find_element_by_css_selector('#category-tree-wrap > ul > li:nth-child(7) > div > span:nth-child(3)').click() # 스포츠
        #driver.find_element_by_css_selector('#category-tree-wrap > ul > li:nth-child(8) > div > span:nth-child(3)').click() # IT_과학

        driver.find_element_by_css_selector('#news-search-form > div > div > div > div.input-group.main-search__form > span > button').click() # 검색 버튼

        time.sleep(1)

        driver.find_element_by_css_selector('#filter-tm-use').click()   #   인사, 부고, 동정, 포토 제외

        time.sleep(1)

        driver.find_element_by_css_selector('#select1 > option:nth-child(3)').click()   # 과거순

        time.sleep(1)

        driver.find_element_by_css_selector('#select2 > option:nth-child(4)').click()   # 100건씩 보기

        time. sleep(1)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        total_count = soup.select_one('#total-news-cnt').get_text().replace(',', '') # 날짜 범위 내 기사 개수
        page_count = (int(total_count) // 100)  # 기사 개수 // 100건씩 보기 = 페이지
        if int(total_count) % 100 != 0:
            page_count += 1
        
        for page in range(1, page_count + 1):   # 1~마지막 페이지
            # 페이지 처리
            time.sleep(1)
            page_click = page % 7   # 페이지 버튼 7개
            if page_click != 1:
                if page_click == 0:
                    page_click = 7
                page_click += 2
                #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#news-results-pagination > ul > li:nth-child(' + str(page_click) + ') > a')))
                try:
                    a = driver.find_element_by_css_selector('#news-results-pagination > ul > li:nth-child(' + str(page_click) + ') > a')    # 페이지 클릭
                    a.click()
                except exceptions.StaleElementReferenceException:
                    a = driver.find_element_by_css_selector('#news-results-pagination > ul > li:nth-child(' + str(page_click) + ') > a')    # 페이지 클릭
                    a.click()
                except exceptions.ElementClickInterceptedException:
                    a = driver.find_element_by_css_selector('#news-results-pagination > ul > li:nth-child(' + str(page_click) + ') > a')
                    a.click()
            elif (page_click == 1) and (page > 1):
                #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#news-results-pagination > ul > li:nth-child(10) > a')))
                try:
                    b = driver.find_element_by_css_selector('#news-results-pagination > ul > li:nth-child(10) > a')  # 다음 목록으로 넘어가기 클릭
                    b.click()
                except exceptions.StaleElementReferenceException:
                    b = driver.find_element_by_css_selector('#news-results-pagination > ul > li:nth-child(10) > a')  # 다음 목록으로 넘어가기 클릭
                    b.click()
                except exceptions.ElementClickInterceptedException:
                    b = driver.find_element_by_css_selector('#news-results-pagination > ul > li:nth-child(' + str(page_click) + ') > a')
                    b.click()
                '''if page != page_count:
                    time.sleep(2)
                    driver.find_element_by_css_selector('#news-results-pagination > ul > li:nth-child(3) > a').click()'''

            time.sleep(2)
        
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            url = soup.select('#news-results > div > div > div > a')  # 기사 url 긁기
            press = soup.select('#news-results > div > div > div > a') # 언론사 긁기
            category = soup.select('#news-results > div > div.news-item__body > div.news-item__meta > span.news-item__category') # 카테고리 긁기
            headline = soup.select('#news-results > div > div.news-item__body > h4') # 기사 제목 긁기
            date = soup.select('#news-results > div > div.news-item__body > div.news-item__meta > span.news-item__date') # 날짜 긁기

            # print(len(date))
            # print(len(url))
            # print(len(press))
            # print(len(category))
            # print(len(headline))

            for w in range(0, len(url)):    # url 수만큼 반복
                self.news_url.append(url[w].get('href'))
            for x in range(0, len(press)):
                self.news_press.append(press[x].text.strip())
            for y in range(0, len(date)):
                if 'Invalid' in date[y].text.strip():
                    continue
                split_category = re.split('>|\|', category[y].text)
                temp_category = []
                for count in range(0, len(split_category), 2):
                    if split_category[count].strip() not in temp_category:
                        temp_category.append(split_category[count].strip())
                self.news_category.append(temp_category)
                self.news_headline.append((headline[y].text).replace('\n', '').replace('>', '').strip())
                self.news_date.append(date[y].text.strip())
        driver.close()

        # print(len(self.news_date))
        # print(len(self.news_url))
        # print(len(self.news_press))
        # print(len(self.news_category))
        # print(len(self.news_headline))

        delete_count = 0    # 문화 카테고리 뉴스 전부 제외
        for z in range(0, len(self.news_category)):
            if "문화" in self.news_category[z - delete_count]:
                self.delete(z - delete_count)
                delete_count += 1

    def save_data(self, date_start, date_end):    # 크롤한 정보들 CSV로 저장
        file = open(date_start + '-' + date_end + '.csv', 'w', encoding='utf-8', newline = '')
        writer = csv.writer(file)
        writer.writerow(["press", "category", "headline", "url", "date"])
        for l in range(0, len(self.news_url)):
            str_category = ''
            for category in self.news_category[l]:
                if category != self.news_category[l][0]:
                    str_category += ','
                str_category += category
            writer.writerow([self.news_press[l], str_category, self.news_headline[l], self.news_url[l], self.news_date[l]])
        file.close()

if __name__ == "__main__":
    temp_start1 = '20191219'
    temp_end1 = '20191231'

    list_date1 = date_calculate(temp_start1, temp_end1)

    for date1 in list_date1:
        temp_date1 = str(date1.year)
        if len(str(date1.month)) == 1:
            temp_date1 += '0'
        temp_date1 += str(date1.month)
        if len(str(date1.day)) == 1:
            temp_date1 += '0'
        temp_date1 += str(date1.day)

        print(temp_date1)
        Crawler1 = Big_Kinds_Crawler()
        Crawler1.crawl_news_url(date1, date1)
        Crawler1.save_data(temp_date1, temp_date1)
