from flask import Blueprint, session, render_template, request, url_for, jsonify, current_app
from decorator import check_login, check_finished_exam, check_start_exam, check_match_time, check_init_match
from exts import r, app
from module import Score, db
import time

exam = Blueprint("exam", __name__)

# 答题
@exam.route('/exam', endpoint="exam")
@check_login
@check_init_match
@check_finished_exam
@check_match_time
def exam_():
    if r.hexists("user:"+session["user"], "start_time"):
        all_question_id = r.lrange("user_question_id:"+session["user"], 0, r.llen("user_question_id:"+session["user"]))
    else:
        r.hset("user:"+session["user"], "start_time", int(time.time()))
        all_question_id = r.srandmember("all_question_id", current_app.config["once_exam_nums"])
        for i in all_question_id:
            r.rpush("user_question_id:"+session["user"], i)
    questions = []
    for q_id in all_question_id:
        description = r.hget("question[%s]" % q_id, "description")
        answerA = r.hget("question[%s]" % q_id, "answerA")
        answerB = r.hget("question[%s]" % q_id, "answerB")
        answerC = r.hget("question[%s]" % q_id, "answerC")
        answerD = r.hget("question[%s]" % q_id, "answerD")
        question = {"id": q_id, "description": description, "answerA": answerA, "answerB": answerB, "answerC": answerC, "answerD": answerD}
        questions.append(question)
    return render_template("exam.html", match_name=app.config['match_name'], questions=questions)

# 交卷检查
@exam.route("/check_answers", endpoint="check_answers", methods=["POST"])
@check_login
@check_init_match
@check_start_exam
@check_finished_exam
@check_match_time
def check_answers():
    score = 0
    for q in request.form:
        if "question" in q:
            if r.hexists(q, "answer"):
                if request.form.get(q) == r.hget(q, "answer"):
                    score += app.config['one_question_score']

    finish_time = int(time.time())
    start_time = int(r.hget("user:"+session["user"], "start_time"))
    spend_time = finish_time - start_time
    try:
        add_score = Score(username=session["user"], score=score, finish_time=finish_time, start_time=start_time, spend_time=spend_time)
        db.session.add(add_score)
        db.session.commit()
        r.hset("user:"+session["user"], "score", score)
        r.hset("user:"+session["user"], "finish_time", finish_time)
        r.hset("user:"+session["user"], "spend_time", spend_time)
        status_code = 200
        message = "交卷成功"
    except:
        status_code = 300
        message = "交卷失败"
    callback_type = "forward"
    url = url_for("display.result")
    res = '{"statusCode": %s,"message": "%s","callbackType": "%s","forwardUrl": "%s"}' % (status_code, message, callback_type, url)
    return res

# 计时器，已经过去的时间
@exam.route("/match_time", endpoint="match_time")
@check_login
@check_init_match
@check_start_exam
@check_finished_exam
@check_match_time
def match_time():
    left_time = int(time.time()) - int(r.hget("user:"+session["user"], "start_time"))
    return jsonify({"match_duration": app.config['match_duration'], "left_time": left_time})

# 保存用户的答案
@exam.route("/save_user_answer", endpoint="save_user_answer", methods=["POST"])
@check_login
@check_init_match
@check_start_exam
@check_finished_exam
@check_match_time
def save_user_answer():
    try:
        for post in request.form:
            if "question" in post:
                r.hset("user:"+session["user"], post, request.form.get(post))  # question[id]
        return '{"statusCode": 200}'
    except:
        return '{"statusCode": 300}'

# 标记题目
@exam.route("/sign_mark", endpoint="sign_mark")
@check_login
@check_init_match
@check_start_exam
@check_finished_exam
@check_match_time
def sign_mark():
    try:
        if r.hexists("user:"+session["user"], "mark"+request.args.get('questionid')):
            if r.hget("user:"+session["user"], "mark"+request.args.get('questionid')) == "1":
                r.hset("user:" + session["user"], "mark"+request.args.get('questionid'), 0)
                return "0"  # 取消标记
        r.hset("user:"+session["user"], "mark"+request.args.get('questionid'), 1)
        return "1"   # 标记
    except:
        return "error"

# 加载用户的数据
@exam.route("/load_user_data", endpoint="load_user_data")
@check_login
@check_init_match
@check_start_exam
@check_finished_exam
@check_match_time
def load_user_data():
    res = {}
    all_question_id = r.lrange("user_question_id:"+session["user"], 0, r.llen("user_question_id:"+session["user"]))
    for i in all_question_id:
        res[i] = {"checked": 0, "mark": 0}
        if r.hexists("user:"+session["user"], "question[%s]" % i):
            user_choise = r.hget("user:"+session["user"], "question[%s]" % i)
            res[i]["checked"] = user_choise
        if r.hexists("user:"+session["user"], "mark%s" % i):
            if r.hget("user:"+session["user"], "mark%s" % i) == "1":
                res[i]["mark"] = 1
    return jsonify(res)
