import pymysql 
import datetime


#데이터베이스 접속
conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='tweather', charset='utf8')
curs = conn.cursor()


class Analize:
    # 생성자 : 테이블 이름
    def __init__(self, table_name):
        self.table_name = table_name
        self.current_time_f = datetime.datetime.now().strftime('%Y-%m-%d')

    # 현재 시간
    def current_time(self):
        current_datetime = datetime.datetime.now()
        return current_datetime


    # 내일, 모레등 날짜 계산
    def date_add(self,today_time,num):
        past_datetime = today_time + datetime.timedelta(days=num)
        return past_datetime


    # 데이터베이스에서 데이터를 가져온다.
    def bring_db(self,n): 
        today_date = self.current_time()
        today_date_t = today_date.strftime('%Y-%m-%d')
        check_time = self.date_add(today_date, n).strftime('%Y-%m-%d')


        #curs.execute('select weather_c FROM '+self.table_name+" WHERE measurement='{}' and real_date='{}'".format(check_time, today_date_t))
        curs.execute('select weather_c FROM '+self.table_name+" WHERE measurement='{}' and real_date='{}'".format(check_time, today_date_t))
        condition_data= curs.fetchone()
        conn.commit()

        return condition_data[0]


    # 가져온 데이터에 비나 소나기등 강수예보가 있는지 확인. 있으면 1, 없으면 -1을 반환
    def check_condition(self, information):
        t_f = information.find("비")
        t_f2 = information.find("소나기")
        t_f3 = information.find("눈")
        
        if t_f == -1 and t_f2 == -1 and t_f3 == -1:
            return -1
        else:
            return 1

    
    # 비교한 데이터를 데이터베이스에 저장
    def save_db(self, today, compare, c_n):
        curs.execute("select measurement from "+self.table_name+"_ts where measurement='{}'".format(self.current_time_f))
        check = curs.fetchone()
        conn.commit()

        if check != None:
            if today == 1 and compare == 1:
                curs.execute("update "+self.table_name+"_ts SET H_"+str(c_n)+"=1 WHERE measurement='{}'".format(self.current_time_f))
                conn.commit()

            elif today == 1 and compare == -1:
                curs.execute("update "+self.table_name+"_ts SET M_"+str(c_n)+"=1 WHERE measurement='{}'".format(self.current_time_f))
                conn.commit()

            elif today == -1 and compare == 1:
                curs.execute("update "+self.table_name+"_ts SET F_"+str(c_n)+"=1 WHERE measurement='{}'".format(self.current_time_f))
                conn.commit()

            else:
                curs.execute("update "+self.table_name+"_ts SET F_"+str(c_n)+"=0 WHERE measurement='{}'".format(self.current_time_f))
                conn.commit()

        else:
            if today == 1 and compare == 1:
                curs.execute("insert into "+self.table_name+"_ts(measurement,H_"+str(c_n)+") values('{}',1)".format(self.current_time_f))
                conn.commit()

            elif today == 1 and compare == -1:
                #curs.execute("insert into "+self.table_name+"_ts(M_"+str(c_n)+",measurement) values(1)")
                curs.execute("insert into "+self.table_name+"_ts(measurement,M_"+str(c_n)+") values('{}',1)".format(self.current_time_f))
                conn.commit()
        
            elif today == -1 and compare == 1:
                #curs.execute("insert into "+self.table_name+"_ts(F_"+str(c_n)+",measurement) values(1)")
                curs.execute("insert into "+self.table_name+"_ts(measurement,F_"+str(c_n)+") values('{}',1)".format(self.current_time_f))
                conn.commit()

            else:
                curs.execute("insert into "+self.table_name+"_ts(measurement,F_"+str(c_n)+") values('{}',0)".format(self.current_time_f))
                conn.commit()

    def calculate_hmf(self):
        for i in range(1,5):
            curs.execute("select H_"+str(i)+" FROM "+self.table_name+"_ts WHERE H_"+str(i)+"=1")
            H = curs.fetchall()
            curs.execute("select M_"+str(i)+" FROM "+self.table_name+"_ts WHERE M_"+str(i)+"=1")
            M = curs.fetchall()
            curs.execute("select F_"+str(i)+" FROM "+self.table_name+"_ts WHERE F_"+str(i)+"=1")
            F = curs.fetchall()
            conn.commit()
            len_h = len(H)
            len_m = len(M)
            len_f = len(F)
            TS = self.calculate_ts(len_h, len_m, len_f)
            curs.execute("UPDATE "+self.table_name+" SET ts_"+str(i)+"='{}' WHERE measurement='{}'".format(round(TS,1),self.current_time_f))

    def calculate_ts(self, h, m, f):
        if h == 0 or (h+m+f) ==0:
            return 0
        else:    
            ts=h/(h+m+f)
            return (ts*100)

    # 메인
    def main(self):
        today_con = self.check_condition(self.bring_db(0)) # 오늘 기상상태
        for i in range(1,5,1): # 전날들의 기상상태를 가져와서 오늘 기상상태랑 비교
            com_con = self.check_condition(self.bring_db(-i))
            self.save_db(today_con, com_con, i)
        
        self.calculate_hmf()


def start(): #시작
    naver = Analize('naver')
    naver.main()
    accuweather = Analize('accuweather')
    accuweather.main()
    """ msn = Analize('msn')
    msn.main() """

if __name__ == "__main__":
    start()