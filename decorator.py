from flask import session, redirect, url_for, render_template
from exts import r, app, str2timestamp
import time


# 检查是否登录
def check_login(func):
    def check():
        try:
            session["user"]
        except:
            return redirect(url_for("user.login"))
        return func()
    return check


# 检查是否已经开始答题，没有答题就去答题页面
def check_start_exam(func):
    def check():
        if not r.hexists("user:" + session["user"], "start_time"):
            return redirect(url_for("exam.exam"))
        return func()
    return check


# 检查是否已经答过题了,如果已经答完题目就去结果页面
def check_finished_exam(func):
    def check():
        if r.hexists("user:"+session["user"], "finish_time"):
            return redirect(url_for("display.result"))
        return func()
    return check


# 比赛时间的检查
def check_match_time(func):
    def check():
        start_time = str2timestamp(app.config['match_start_time'])
        end_time = str2timestamp(app.config['match_end_time'])
        now_time = int(time.time())
        if now_time < start_time:
            # 未开始
            match_time_left = (start_time-now_time)/60
            data = {
                "match_name": app.config['match_name'],
                "match_not_start": True,
                "match_time_left": match_time_left
            }
            return render_template("exam.html", **data)
        elif now_time > end_time:
            # 已结束
            if r.hexists("user:"+session["user"], "start_time"):
                return func()
            else:
                r.hset("user:"+session["user"], "score", 0)
                r.hset("user:"+session["user"], "start_time", 0)
                r.hset("user:"+session["user"], "finish_time", 0)
                r.hset("user:"+session["user"], "spend_time", 0)
                return redirect(url_for("display.score_board"))
        else:
            # 进行中
            return func()
    return check


# 检查是否是管理员
def check_is_admin(func):
    def check():
        if session["is_admin"]:
            return func()
        return "admin only"
    return check


# 检查管理员是否配置了比赛信息
def check_init_match(func):
    def check():
        if app.config["match_start_time"] == '0':
            return "管理员设置开始时间"
        if app.config["match_duration"] == 0:
            return "管理员未设置做题时间"
        if app.config["once_exam_nums"] == 0:
            return "管理员未设置题目数量"
        if app.config["one_question_score"] == 0:
            return "管理员未设置每题分值"
        return func()
    return check
