from flask import Flask
from redis import ConnectionPool, StrictRedis
from os import urandom
import time
from datetime import datetime
from pytz import timezone, utc


# 字符串转时间戳
def str2timestamp(date_str):
    time_array = time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    tz = timezone('Asia/Shanghai')
    y, m, d, H, M, S = time_array[0:6]
    dt = datetime(y, m, d, H, M, S)
    t = tz.localize(dt).astimezone(utc)
    return int(time.mktime(t.utctimetuple())) - time.timezone


# 时间戳转字符串
def timestamp2str(timestamp):
    tz = timezone('Asia/Shanghai')  # 东八区
    date_str = datetime.fromtimestamp(int(timestamp), tz).strftime('%Y-%m-%d %H:%M:%S')  # 提交时间
    return date_str


# 秒数转字符串
def sec2str(sec):
    time_h = sec // 3600
    time_m = (sec % 3600) // 60
    time_s = (sec % 60)
    time_str = "%s时%s分%s秒" % (time_h, time_m, time_s)
    return time_str


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/exam?charset=utf8mb4'
app.config['SECRET_KEY'] = urandom(24)

pool = ConnectionPool(host="127.0.0.1", port=6379, decode_responses=True)
r = StrictRedis(connection_pool=pool, charset="utf8")
