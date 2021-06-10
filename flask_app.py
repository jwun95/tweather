from flask import request, redirect, render_template, url_for, Flask, flash
import pymysql 
from datetime import datetime
from weather import naver_com, accuweather_com, msn_com
from data_analize import analize

app = Flask(__name__)

conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='tweather', charset='utf8')
curs = conn.cursor()

app.debug = True
@app.route('/')
def index():
    naver_com.naver_weather()
    accuweather_com.accuweather_com()
    #msn_com.msn_com()
    analize.start()
    measure = datetime.date(datetime.today())  # 측정날짜
    curs.execute('select * FROM naver WHERE measurement=%s',measure)
    naver_data = curs.fetchall()
    curs.execute('select * FROM accuweather WHERE measurement=%s',measure)
    accu_data = curs.fetchall()
    """ curs.execute('select * FROM msn WHERE measurement=%s',measure)
    msn_data = curs.fetchall() """
    conn.commit()
    return render_template('index.html', naver_data=naver_data, accu_data=accu_data)

if __name__ == "__main__":
    app.run()