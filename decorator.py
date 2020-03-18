from flask import session, redirect, url_for, render_template
from exts import r, app, str2timestamp
import time


# 检查是否登录 【未登录 --> user.login】
def check_login(func):
    def check():
        try:
            session["user"]
        except:
            return redirect(url_for("user.login"))
        return func()
    return check


# 检查是否已经开始答题 【未开始答题 --> exam.exam】
def check_start_exam(func):
    def check():
        if not r.hexists("user:" + session["user"], "start_time"):
            return redirect(url_for("exam.exam"))
        return func()
    return check


# 检查是否已经答过题了 【已经完成了题目 --> display.result】
def check_finished_exam(func):
    def check():
        if r.hexists("user:"+session["user"], "finish_time"):
            return redirect(url_for("display.result"))
        return func()
    return check


# 检查是否超出了最大答题时长 【超出了设置的答题时长 --> exam.check_answers】
def check_timeout(func):
    def check():
        has_started = r.hexists("user:"+session["user"], "start_time")
        has_finished = r.hexists("user:"+session["user"], "finish_time")
        if has_started and not has_finished:
            start_time = int(r.hget("user:"+session["user"], "start_time"))
            now_time = int(time.time())
            spend_time = now_time - start_time
            if spend_time > app.config["match_duration"]*60:      # 答题时长超出了设置的答题时长
                return redirect(url_for("exam.check_answers"))
            else:
                return func()
        return func()
    return check


# 比赛状态的检查 【结束了但还未开始答题 --> display.score_board、未开始 --> 倒计时、没有正确配置 --> "管理未正确配置比赛"】
def check_match_status(func):
    def check_match_time():
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
            if r.hexists("user:"+session["user"], "start_time"):  # 结束但已经开始答题了，继续答题
                return func()
            else:                                                 # 结束了但还未开始答题
                r.hset("user:"+session["user"], "score", 0)
                r.hset("user:"+session["user"], "start_time", 0)
                r.hset("user:"+session["user"], "finish_time", 0)
                r.hset("user:"+session["user"], "spend_time", 0)
                return redirect(url_for("display.score_board"))
        else:
            # 进行中
            return func()

    def check():
        if app.config["match_start_time"] != '0':
            if app.config["match_duration"] != 0:
                if app.config["once_exam_nums"] != 0:
                    if app.config["one_question_score"] != 0:
                        return check_match_time()
        return "管理未正确配置比赛"

    return check


# 检查是否是管理员 【不是管理员 --> 'admin only'】
def check_is_admin(func):
    def check():
        if session["is_admin"]:
            return func()
        return "admin only"
    return check

