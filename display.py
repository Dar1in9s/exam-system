from flask import Blueprint, session, redirect, url_for, render_template, request
from decorator import check_login, check_match_status
from module import Score
from exts import r, app, sec2str, timestamp2str

display = Blueprint("display", __name__)

# 答题结果展示 【已登录，比赛状态正常，已完成】
# exam.exam、display.score_board --> this
# this --> exam.exam、user.login
@display.route("/result", endpoint="result")
@check_login
@check_match_status
def result():
    if not r.hexists("user:"+session["user"], "finish_time"):
        return redirect(url_for("exam.exam"))
    if int(r.hget("user:"+session["user"], "finish_time")) == 0:    # 答题时间已过
        data = {
            'march_name': app.config['match_name'],
            'end_time': app.config['match_end_time'],
            'score': 0,
            'spend_time': 0,
            'total_score': app.config['total_score'],
            'once_exam_nums': app.config['once_exam_nums'],
            'question_right_num': 0
        }
    else:
        spend_time_sec = int(r.hget("user:"+session["user"], "finish_time")) - int(r.hget("user:"+session["user"], "start_time"))
        spend_time = sec2str(spend_time_sec)
        score = int(r.hget("user:" + session["user"], "score"))
        data = {
            'march_name': app.config['match_name'],
            'end_time': app.config['match_end_time'],
            'score': score,
            'spend_time': spend_time,
            'total_score': app.config['total_score'],
            'once_exam_nums': app.config['once_exam_nums'],
            'question_right_num': score // app.config['one_question_score']
        }
    return render_template("result.html", **data)

# 排行榜
# user.login、display.result --> this
# this --> display.result
@display.route("/score_board", endpoint="score_board")
def score_board():
    try:
        page = abs(int(request.args.get("page")))
        if page == 0:
            page = 1
    except:
        page = 1
    begin = (page - 1) * 10
    result = Score.query.order_by(Score.score.desc(), Score.spend_time).limit(10).offset(begin).all()
    users = []
    for i in result:
        spend_time_sec = int(int(i.finish_time) - int(i.start_time))
        spend_time = sec2str(spend_time_sec)
        finish_time =timestamp2str(int(i.finish_time))
        user_tmp = {
            "username": i.username,
            "ranking": begin + 1,
            "score": i.score,
            "finish_time": finish_time,
            "spend_time": spend_time
        }
        begin += 1
        users.append(user_tmp)

    all_nums = Score.query.count()  # 总的提交人数
    try:
        username = session["user"]
        if r.hexists("user:" + session["user"], "score"):
            score = int(r.hget("user:" + session["user"], "score"))
            users_more = Score.query.filter(Score.score >= 0).order_by(Score.score.desc(), Score.spend_time).all()
            ranking = 1
            for i in users_more:
                if i.username == username:
                    break
                ranking += 1
        else:
            score = 0
            ranking = 0
    except:
        score = 0
        ranking = 0

    res = {
        "users": users,
        "all_nums": all_nums,
        "score": score,
        "ranking": ranking,
        "march_name": app.config['match_name'],
        "end_time": app.config['match_end_time']
    }
    return render_template("score_board.html", **res)
