#-*- coding: euc-kr -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import re
import csv

class Big_Kinds_Crawler(object):
    def __init__(self):
        self.news_press = [] # ��л�
        self.news_category = [] # ���� ī�װ�
        self.news_headline = [] # ���� ������
        self.news_url = []  # ���� url
        self.news_main_text = []    # ���� ����
        self.news_date = []  # ���� ��¥

    @staticmethod
    def preprocess(text):
        text = re.sub('<.+?>|&nbsp;|br|��|��|��|��|��|��|��|��|��|  ', '', str(text))
        text = text.replace("\n", "")
        text = text.strip()
        return text

    def delete(self, url_count):
        del self.news_press[url_count]
        del self.news_category[url_count]
        del self.news_headline[url_count]
        del self.news_url[url_count]
        del self.news_date[url_count]

    def crawl_news_url(self, date_start, date_end):   # ��ī����� ������ url, ��л�, ������, ��¥, ī�װ� ũ��

        driver = webdriver.Chrome('/Users/geun/KoreanNewsChronicle/Crawling/chromedriver')
        driver.implicitly_wait(3)
        driver.get('https://www.bigkinds.or.kr/')

        driver.implicitly_wait(1)

        # �˾� â �ݱ�
        '''html_popup = driver.page_source
        soup_popup = BeautifulSoup(html_popup, 'html.parser')
        if soup_popup.select('#contents > div.popup-container') != None:
            driver.find_element_by_css_selector('div.popup-footer > div > div > button').click()'''
            
        # �Ⱓ ����
        driver.find_element_by_id('date-filter-btn').click()    # �Ⱓ ��ư
        #driver.find_element_by_css_selector('#date-filter-div > div > div:nth-child(1) > button:nth-child(1)').click() # 1�� ��ư
        #driver.find_element_by_css_selector('#date-filter-div > div > div:nth-child(1) > button:nth-child(2)').click() # 1�� ��ư
        #driver.find_element_by_css_selector('#date-filter-div > div > div:nth-child(1) > button:nth-child(3)').click() # 1���� ��ư
        #driver.find_element_by_css_selector('#date-filter-div > div > div:nth-child(1) > button:nth-child(4)').click() # 3���� ��ư
        #driver.find_element_by_css_selector('#date-filter-div > div > div:nth-child(1) > button:nth-child(5)').click() # 6���� ��ư
        #driver.find_element_by_css_selector('#date-filter-div > div > div:nth-child(1) > button:nth-child(6)').click() # 1�� ��ư
        driver.find_element_by_id('search-begin-date').send_keys('\b\b\b\b\b\b\b\b\b\b' + date_start[0:4] + '-' + date_start[4:6] + '-' + date_start[6:]) # ���� ��¥ �Է�
        driver.find_element_by_id('search-end-date').send_keys('\b\b\b\b\b\b\b\b\b\b' + date_end[0:4] + '-' + date_end[4:6] + '-' + date_end[6:])   # �� ��¥ �Է�
        driver.find_element_by_id('date-confirm-btn').click()   # �Ⱓ ���� ��ư

        # ��л� ����
        driver.find_element_by_id('provider-filter-btn').click()    # ��л� ��ư  
        #driver.find_element_by_id('�߾���').click()    # �߾��� üũ�ڽ�
        #driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(1) > div > button:nth-child(1)').click()    # ����
        driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(2)').click()    # ����
        driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(3)').click()    # ����
        driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(4)').click()    # ����
        driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(5)').click()    # ��ȭ
        driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(6)').click()    # ����
        driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(7)').click()    # ����
        #driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(8)').click()    # ����
        driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(9)').click()    # �߾�
        driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(10)').click()   # �Ѱܷ�
        driver.find_element_by_css_selector('#providers-wrap > div:nth-child(3) > div:nth-child(2) > div > button:nth-child(11)').click()   # �ѱ�

        driver.implicitly_wait(1)

        # ī�װ� ����
        driver.find_element_by_id('category-filter-btn').click()    # ī�װ� ��ư
        driver.find_element_by_css_selector('#category-tree-wrap > ul > li:nth-child(1) > div > span:nth-child(3)').click() # ��ġ
        driver.find_element_by_css_selector('#category-tree-wrap > ul > li:nth-child(2) > div > span:nth-child(3)').click() # ����
        driver.find_element_by_css_selector('#category-tree-wrap > ul > li:nth-child(3) > div > span:nth-child(3)').click() # ��ȸ
        #driver.find_element_by_css_selector('#category-tree-wrap > ul > li:nth-child(4) > div > span:nth-child(3)').click() # ��ȭ
        driver.find_element_by_css_selector('#category-tree-wrap > ul > li:nth-child(5) > div > span:nth-child(3)').click() # ����
        #driver.find_element_by_css_selector('#category-tree-wrap > ul > li:nth-child(6) > div > span:nth-child(3)').click() # ����
        #driver.find_element_by_css_selector('#category-tree-wrap > ul > li:nth-child(7) > div > span:nth-child(3)').click() # ������
        #driver.find_element_by_css_selector('#category-tree-wrap > ul > li:nth-child(8) > div > span:nth-child(3)').click() # IT_����

        driver.find_element_by_css_selector('#news-search-form > div > div > div > div.input-group.main-search__form > span > button').click() # �˻� ��ư

        driver.implicitly_wait(3)

        driver.find_element_by_css_selector('#filter-tm-use').click()   #   �λ�, �ΰ�, ����, ���� ����

        time.sleep(1)

        driver.find_element_by_css_selector('#select1 > option:nth-child(3)').click()   # ���ż�

        time.sleep(1)

        driver.find_element_by_css_selector('#select2 > option:nth-child(4)').click()   # 100�Ǿ� ����

        time. sleep(1)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        total_count = soup.select_one('#total-news-cnt').get_text().replace(',', '') # ��¥ ���� �� ��� ����
        page_count = (int(total_count) // 100)  # ��� ���� // 100�Ǿ� ���� = ������
        if int(total_count) % 100 != 0:
            page_count += 1
        
        for page in range(1, page_count + 1):   # 1~������ ������
            # ������ ó��
            
            page_click = page % 7   # ������ ��ư 7��
            if page_click != 1:
                if page_click == 0:
                    page_click = 7
                page_click += 2
                driver.find_element_by_css_selector('#news-results-pagination > ul > li:nth-child(' + str(page_click) + ') > a').click()    # ������ Ŭ��
            elif (page_click == 1) and (page > 1):
                driver.find_element_by_css_selector('#news-results-pagination > ul > li:nth-child(10) > a').click()  # ���� ������� �Ѿ�� Ŭ��
                '''if page != page_count:
                    time.sleep(2)
                    driver.find_element_by_css_selector('#news-results-pagination > ul > li:nth-child(3) > a').click()'''

            time.sleep(2)
        
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            url = soup.select('#news-results > div > div > div > a')  # ��� url �ܱ�
            press = soup.select('#news-results > div > div > div > a') # ��л� �ܱ�
            category = soup.select('#news-results > div > div.news-item__body > div.news-item__meta > span.news-item__category') # ī�װ� �ܱ�
            headline = soup.select('#news-results > div > div.news-item__body > h4') # ��� ���� �ܱ�
            date = soup.select('#news-results > div > div.news-item__body > div.news-item__meta > span.news-item__date') # ��¥ �ܱ�

            for w in range(0, len(url)):    # url ����ŭ �ݺ�
                self.news_url.append(url[w].get('href'))
            for x in range(0, len(press)):
                self.news_press.append(press[x].text)
            for y in range(0, len(date)):
                if 'Invalid' in date[y].text.strip():
                    continue
                split_category = re.split('>|\|', category[y].text)
                temp_category = []
                for count in range(0, len(split_category), 2):
                    if split_category[count].strip() not in temp_category:
                        temp_category.append(split_category[count].strip())
                self.news_category.append(temp_category)
                self.news_headline.append((headline[y].text).replace('>', '').strip())
                self.news_date.append(date[y].text.strip())
        driver.close()

    def crawl_news_text(self):  # �ܾ�� url�� ���� ���� ���� �ܱ�
        fail_count = 0  # url�� ���� ������ ���� �� count
        for url_count  in range(0, len(self.news_url)): # ��ī����� �ܾ�� url ����ŭ ��
            url_html = requests.get(self.news_url[url_count - fail_count]).content
            soup = BeautifulSoup(url_html, 'html.parser')
            #print(self.news_url[url_count - fail_count])
            # �� ����� ��л翡 �°� ũ��
            #if '����Ź�' in self.news_press[url_count]:
            #    self.news_main_text.append(self.preprocess(soup.select_one('#articleBody').get_text()))
            if '�����Ϻ�' in self.news_press[url_count - fail_count]:
                tag = soup.select_one('#articleBody')
                if tag == None:    # url�� ���� ���� ���� ��
                    self.delete(url_count - fail_count) # ��� list���� �ش� url�� ���� ���� ����
                    fail_count += 1
                else:
                    self.news_main_text.append(self.preprocess(tag.text))
            elif '���ϽŹ�' in self.news_press[url_count - fail_count]:
                tag = soup.select_one('#contents > p')
                if tag == None:
                    self.delete(url_count - fail_count)
                    fail_count += 1
                else:
                    self.news_main_text.append(self.preprocess(tag.text))
            elif '�����Ϻ�' in self.news_press[url_count - fail_count]:
                tag = soup.select_one('#content > div > div.article_txt')
                if tag == None:
                    self.delete(url_count - fail_count)
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
                    self.news_main_text.append(self.preprocess(tag.text))
            elif '��ȭ�Ϻ�' in self.news_press[url_count - fail_count]:
                tag = soup.select_one('#NewsAdContent')
                if  tag == None:
                    self.delete(url_count - fail_count)
                    fail_count += 1
                else:
                    self.news_main_text.append(self.preprocess(tag.text))
            elif '����Ź�' in self.news_press[url_count - fail_count]:
                if 'go' in self.news_url[url_count - fail_count]:
                    tag = soup.select_one('#article_content')
                    if tag == None:
                        self.delete(url_count - fail_count)
                        fail_count += 1
                    else:
                        self.news_main_text.append(self.preprocess(tag.text))
                elif 'now' in self.news_url[url_count - fail_count]:
                    tag = soup.select_one('#articleContent')
                    if tag == None:
                        self.delete(url_count - fail_count)
                        fail_count += 1
                    else:
                        self.news_main_text.append(self.preprocess(tag.text))
                elif 'stv' in self.news_url[url_count - fail_count]:
                    tag = soup.select_one('#CmAdContent')
                    if tag == None:
                        self.delete(url_count - fail_count)
                        fail_count += 1
                    else:
                        self.news_main_text.append(self.preprocess(tag.text))
                elif 'biz' in soup.select_one('link').get('href'):
                    tag = soup.select_one('body > div > div.middleWrap > div > div.mLeftWrap > div.articleDiv')
                    if tag == None:
                        self.delete(url_count - fail_count)
                        fail_count += 1
                    else:
                        self.news_main_text.append(self.preprocess(tag.text))
                else:
                    tag = soup.select_one('#atic_txt1')
                    if tag == None:
                        self.delete(url_count - fail_count)
                        fail_count += 1
                    else:
                        self.news_main_text.append(self.preprocess(tag.text))
            elif '�����Ϻ�' in self.news_press[url_count - fail_count]:
                tag = soup.select_one('#article_txt > article')
                if tag == None:
                        self.delete(url_count - fail_count)
                        fail_count += 1
                else:
                    for figure in tag.select('figure'):
                        figure.decompose()
                    self.news_main_text.append(self.preprocess(tag.text))
            #elif '�����Ϻ�' in self.news_press[url_count - fail_count]:
            #    self.news_main_text.append(self.preprocess(soup.select_one('#articleBody').get_text()))
            elif '�߾��Ϻ�' in self.news_press[url_count - fail_count]:
                tag = soup.select_one('#article_body')
                if tag == None:
                        self.delete(url_count - fail_count)
                        fail_count += 1
                else:
                    for div in tag.select('div'):
                        div.decompose()
                    self.news_main_text.append(self.preprocess(tag.text))
            elif '�Ѱܷ�' in self.news_press[url_count - fail_count]:
                tag = soup.select_one('div.article-text > div > div.text')
                if tag == None:
                    self.delete(url_count - fail_count)
                    fail_count += 1
                else :
                    for div in tag.select('div'):
                        div.decompose()
                    self.news_main_text.append(self.preprocess(tag.text))
            elif '�ѱ��Ϻ�' in self.news_press[url_count - fail_count]:
                tag = soup.select_one('body > div.wrap > div.container.end > div > div > div > p')
                if tag  == None:
                        self.delete(url_count - fail_count)
                        fail_count += 1
                else:
                    text = ""
                    result_set = soup.select('body > div.wrap > div.container.end > div > div > div > p')
                    for p in result_set:
                       text = text + p.text   
                    self.news_main_text.append(self.preprocess(text).replace('user@hankookilbo.com������ ���', ''))

    def save_data(self, date_start, date_end):    # ũ���� ������ CSV�� ����
        file = open(date_start + '-' + date_end + '.csv', 'w', encoding='utf-8', newline = '')
        writer = csv.writer(file)
        writer.writerow(["date", "category", "headline", "url", "text"])
        for l in range(0, len(self.news_url)):
            str_category = ''
            for category in self.news_category[l]:
                if category != self.news_category[l][0]:
                    str_category += ','
                str_category += category
            writer.writerow([self.news_date[l], str_category, self.news_headline[l], self.news_url[l], self.news_main_text[l]])
        file.close()
    
if __name__ == "__main__":
    date_start = str(input('���� ��¥ �Է� ex) 20200905 : '))
    date_end = str(input('�� ��¥ �Է� ex) 20200909 : '))

    Crawler = Big_Kinds_Crawler()
    Crawler.crawl_news_url(date_start, date_end)
    Crawler.crawl_news_text()
    Crawler.save_data(date_start, date_end)
