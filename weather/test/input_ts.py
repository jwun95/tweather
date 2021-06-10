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
        ran = random.randint(0, 1)
        return ran

    def ran2(self):
        ran = random.randint(0, 1)
        return ran

    def ran3(self):
        ran = random.randint(0, 1)
        if ran == 0:
            return 0
        else:
            return 1

    def start_test(self):
        current_time = datetime.datetime.now()

        for my_n in range(1, 10):
            measure = self.time(current_time, -my_n)
            
            for mynum in range(1, 5):
                data_ran = self.ran()
                data_ran2 = self.ran2()
                data_ran3 = self.ran3()

                #print(data_ran, data_ran2, data_ran3)
                """ curs.execute("select measurement from "+self.table_name+" where measurement='{}'".format(measure.strftime('%Y-%m-%d')))
                check = curs.fetchone()
                conn.commit()

                print(check) """

                if mynum == 1:
                    curs.execute("insert into "+self.table_name+"(measurement, H_"+str(mynum)+", M_"+str(mynum)+", F_"+str(mynum)+") values('{}',{}, {}, {})".format(measure.strftime('%Y-%m-%d'),data_ran,data_ran2,data_ran3))
                    conn.commit()
    
                else:
                    curs.execute("UPDATE {} SET H_{}={},M_{}={},F_{}={} where measurement='{}'".format(self.table_name,str(mynum),data_ran,str(mynum),data_ran2,str(mynum),data_ran3,measure.strftime('%Y-%m-%d')))
                    conn.commit()
                


                """ if check is not None:
                    curs.execute(f'UPDATE {self.table_name} SET H_{str(mynum)}={data_ran}, M_{str(mynum)}={data_ran2}, F_{str(mynum)}={data_ran3}')
                    conn.commit()

                else:
                    curs.execute("insert into "+self.table_name+"(measurement, H_"+str(mynum)+", M_"+str(mynum)+", F_"+str(mynum)+") values('{}','{}', '{}', '{}')".format(measure.strftime('%Y-%m-%d'),data_ran,data_ran2,data_ran3))
                    conn.commit() """
                              

def start():
    naver = Test('naver_ts')
    naver.start_test()
    accuweather = Test('accuweather_ts')
    accuweather.start_test()
    #msn = Test('msn_ts')
    #msn.start_test()


if __name__ == "__main__":
    start()