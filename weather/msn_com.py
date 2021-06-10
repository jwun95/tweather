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

def msn_com():
    url = 'https://www.msn.com/ko-kr/weather/today/%eb%85%b8%ec%9b%90%ea%b5%ac,%ec%84%9c%ec%9a%b8%ed%8a%b9%eb%b3%84%ec%8b%9c,%eb%8c%80%ed%95%9c%eb%af%bc%ea%b5%ad/we-city?iso=KR&el=iqSI%2F9WJu%2FskSXsuBm9Xtg%3D%3D'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    weather_list = soup.find("p", attrs={"class":"header-DS-EntryPoint1-1"}).get_text()
    print((weather_list))
    current_datetime = datetime.datetime.now()  # 측정날짜


    count = 0

    curs.execute("select measurement from msn where measurement='{}'".format(current_datetime.strftime(duplicate)))
    check = curs.fetchone()
    conn.commit()
    
    if check == None: # 데이터가 없을 경우에만 실행
        for weather in weather_list:
            
            real_datetime = day_cal(current_datetime, count) # 실제 날짜 기록
            # 5일까지만 계산
            count = count + 1
            if count == 6:
                break

            #날짜
            day = weather.find("div", attrs={"class":"dt"}).find_all("span")[1].get_text() # 요일

            #강수확률
            rain = weather.find("div", attrs={"class":"precipicn"}).get_text()

            #날씨 상태
            weather_c = weather.find("img", attrs={"class":"image skyimg"}).get('alt')#날씨 상태
            
            # 최고 기온 / 최저 기온
            max_t = weather.find("li").find("p").get_text() # 최고기온
            min_t = weather.find("li").find("p", attrs={"class":"transparent"}).get_text() # 최저기온


            curs.execute("insert into msn(measurement,day,rain,weather_c,max_t,min_t,real_date) values(%s,%s,%s,%s,%s,%s,%s)"
            ,(current_datetime.strftime(duplicate),day,md(rain),weather_c,md(max_t),md(min_t),real_datetime.strftime(duplicate)))
            conn.commit()
                  
if __name__ == "__main__":
    msn_com()