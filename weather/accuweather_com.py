import requests, pymysql, re, datetime
from bs4 import BeautifulSoup


conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='tweather', charset='utf8')
curs = conn.cursor()
duplicate = '%Y-%m-%d'

def create_connection(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text,"lxml")
    return soup

def md(dig): #정규식을 통한 숫자만 text값으로 리턴
    dig_c=re.findall(r'-?\d+', dig)[0]
    return dig_c

def day_cal(current_datetime,n): # 실제 날짜 기록
    new_datetime = current_datetime + datetime.timedelta(days=n)
    return new_datetime

def accuweather_com():
    url = 'https://www.accuweather.com/ko/kr/jangam-dong/2002771/daily-weather-forecast/2002771'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    weather_list = soup.find("div", attrs={"class":"page-column-1"}).find_all("div", attrs={"class":"daily-wrapper"})
    current_datetime = datetime.datetime.now()  # 측정날짜

    count = 0

    curs.execute("select measurement from accuweather where measurement='{}'".format(current_datetime.strftime(duplicate)))
    check = curs.fetchone()
    conn.commit()
    
    if check == None: # 데이터가 없을 경우에만 실행
        for weather in weather_list:
            
            real_datetime = day_cal(current_datetime, count) # 실제 날짜 기록
            # 5일까지만 계산
            count = count + 1
            if count == 6:
                break

            day = weather.find("span", attrs={"class":"module-header dow date"}).get_text() # 요일
            date = weather.find("span", attrs={"class":"module-header sub date"}).get_text() # 날짜

            rain = weather.find("div", attrs={"class":"precip"}).get_text() # 강수량
            rain = str.strip(rain)
            if rain =="":
                rain="0%"

            weather_c = weather.find("div", attrs={"class":"phrase"}).get_text()#날씨 상태
            weather_c = str.strip(weather_c)

            # 최고 기온 / 최저 기온
            max_t = weather.find("span", attrs={"class":"high"}).get_text() # 최고기온
            min_t = weather.find("span", attrs={"class":"low"}).get_text() # 최저기온


            curs.execute("insert into accuweather(measurement,day,rain,weather_c,max_t,min_t,real_date) values(%s,%s,%s,%s,%s,%s,%s)"
            ,(current_datetime.strftime(duplicate),day,md(rain),weather_c,md(max_t),md(min_t),real_datetime.strftime(duplicate)))
            conn.commit()
                  
if __name__ == "__main__":
    accuweather_com()