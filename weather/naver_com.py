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

def naver_weather():
    url = "https://n.weather.naver.com/"
    soup = create_connection(url)

    weather_list = soup.find("ul", attrs={"class":"week_list"}).find_all("li")
    current_datetime = datetime.datetime.now()  # 측정날짜

    count = 0

    curs.execute("select measurement from naver where measurement='{}'".format(current_datetime.strftime(duplicate)))
    check = curs.fetchone()
    conn.commit()
    
    if check == None: # 데이터가 안에 없을 경우에만 실행
        for weather in weather_list:
            real_datetime = day_cal(current_datetime, count) # 실제 날짜 기록
            count = count + 1
            if count == 6:
                break
            day = weather.find("strong").get_text() # 요일

            #print(day)

            date = weather.find("span", attrs={"class":"date"}).get_text() # 날짜

            #print(date)

            m_a_m = weather.find_all("span", attrs={"class":"timeslot"})[0].get_text() # morning 오전표시
            m_a_a = weather.find_all("span", attrs={"class":"timeslot"})[1].get_text() # afternoon 오후표시

            rain = weather.find_all("span", attrs={"class":"rainfall"})[0].get_text() # 오전 강수확률
            rain_a = weather.find_all("span", attrs={"class":"rainfall"})[1].get_text() # 오후 강수확률

            weather_c = weather.find_all("i")[0].get_text() # 오전 날씨 상태
            weather_c_a = weather.find_all("i")[1].get_text() # 오후 날씨 상태

            # 최고 기온 / 최저 기온
            temperature = weather.find("strong", attrs={"class":"temperature"}).get_text().split('/') # /기준으로 문자열 스플릿
            max_t = temperature[1] # 최고 기온
            min_t = temperature[0] # 최저 기온

            curs.execute("insert into naver(measurement,day,rain,weather_c,max_t,min_t,real_date) values(%s,%s,%s,%s,%s,%s,%s)"
            ,(current_datetime.strftime(duplicate),day,md(rain),weather_c,md(max_t),md(min_t),real_datetime.strftime(duplicate)))
            conn.commit()

                  
if __name__ == "__main__":
    naver_weather()