import pymysql 

conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='tweather', charset='utf8')
curs = conn.cursor()

curs. execute("delete from msn")
curs. execute("delete from msn_ts")
curs. execute("delete from naver")
curs. execute("delete from naver_ts")
curs. execute("delete from accuweather")
curs. execute("delete from accuweather_ts")
conn.commit()