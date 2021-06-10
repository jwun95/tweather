import pymysql 
import datetime
import random

conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='tweather', charset='utf8')
curs = conn.cursor()


class Test:

    def __init__(self, table_name):
        self.table_name = table_name

    def time(self, i_time, num):
        past_datetime = i_time + datetime.timedelta(days=num)
        return past_datetime

    def ran(self):
        ran = random.randint(0, 4)
        weather_c = ['구름많음','비내림','소나기','맑음','흐림']
        return weather_c[ran]

    def start_test(self):
        current_time = datetime.datetime.now()

        for k in range(1, 5):
            measure = self.time(current_time, -k)

            for i in range(0,5):
                data_list = self.ran()
                real_time = self.time(measure, i)
                curs.execute("insert into "+self.table_name+"(measurement, weather_c, real_date) values('{}', '{}', '{}')".format(measure.strftime('%Y-%m-%d'), data_list, real_time.strftime('%Y-%m-%d')))
                #curs.execute("insert into "+self.table_name+"_ts('{}','{}','{}','{}') values('{}','{}','{}','{}')")
                conn.commit()


def start():
    naver = Test('naver')
    naver.start_test()
    accuweather = Test('accuweather')
    accuweather.start_test()
    #msn = Test('msn')
    #msn.start_test()


if __name__ == "__main__":
    start()

