import csv
import re

def preprocess(text):
    text = re.sub('<.+?>|&nbsp;|br|⊙|※|▲|◆|▶|■|●|○|△|□|  ', '', str(text))
    text = text.replace("\n", "")
    text = text.replace("\r", "")
    text = text.strip()
    return text

def save_data(news_press, news_category, news_headline, news_url, news_date, news_main_text):
    
    file_write = open("201909.csv", 'w', encoding='utf-8', newline = '')    # 저장 파일 이름
    
    writer = csv.writer(file_write)
    
    writer.writerow(["date", "press", "category", "headline", "url", "text"])
    
    for l in range(0, len(news_url)):
        news_headline[l] = preprocess(news_headline[l])
        news_main_text[l] = preprocess(news_main_text[l])
        writer.writerow([news_date[l], news_press[l], news_category[l], news_headline[l], news_url[l], news_main_text[l]])
    
    file_write.close()

if __name__ == "__main__":
    news_press = []
    news_category = []
    news_headline = []
    news_url = []
    news_main_text = []
    news_date = []

    num = 6 # 읽어오는 파일 개수

    for i in range(1, num + 1): 
        file_read = open(str(i) + "_201909.csv", "r", encoding='utf-8')     # 읽어오는 파일 이름
     
        rdr = csv.reader(file_read)

        count = 1
        for row in rdr:
            if count == 1:
                count += 1
                continue
            
            news_date.append(row[0])
            news_press.append(row[1])
            news_category.append(row[2])
            news_headline.append(row[3])
            news_url.append(row[4])
            news_main_text.append(row[5])
        
        file_read.close()
    save_data(news_press, news_category, news_headline, news_url, news_date, news_main_text)
    
