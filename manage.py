from flask import Blueprint, url_for, request, render_template, current_app, redirect
from decorator import check_login, check_is_admin
from module import MatchInfo, db, Qeustions, Score, Users, load_match_info, load_questions
from math import ceil
from exts import r

manage = Blueprint("manage", __name__)

# 比赛信息设置
@manage.route("/manage", endpoint="match_info", methods=["GET", "POST"])
@check_login
@check_is_admin
def match_info():
    match = MatchInfo.query.first()
    if request.method == "GET":
        match = match.format()
        info = {
            "match_start_time": match["match_start_time"],
            "match_end_time": match["match_end_time"],
            "match_name": match["match_name"],
            "match_duration": match["match_duration"],
            "one_question_score": match["one_question_score"],
            "once_exam_nums": match["once_exam_nums"]
        }
        return render_template("manage_match_info.html", **info)
    else:
        try:
            match.match_start_time = request.form.get("match_start_time")
            match.match_end_time = request.form.get("match_end_time")
            match.match_name = request.form.get("match_name")
            match.match_duration = request.form.get("match_duration")
            match.one_question_score = request.form.get("one_question_score")
            match.once_exam_nums = request.form.get("once_exam_nums")
            db.session.commit()

            current_app.config["match_start_time"] = request.form.get("match_start_time").replace("T", " ") + ":00"
            current_app.config["match_end_time"] = request.form.get("match_end_time").replace("T", " ") + ":00"
            current_app.config["match_name"] = request.form.get("match_name")
            current_app.config["match_duration"] = abs(int(request.form.get("match_duration")))
            current_app.config["one_question_score"] = abs(int(request.form.get("one_question_score")))
            current_app.config["once_exam_nums"] = abs(int(request.form.get("once_exam_nums")))
            current_app.config['total_score'] = current_app.config['once_exam_nums'] * int(current_app.config['one_question_score'])

            status_code = 200
            message = "保存成功"
        except:
            status_code = 300
            message = "操作失败"
        callback_type = "forward"
        url = url_for("manage.match_info")
        res = '{"statusCode": %s,"message": "%s", "callbackType": "%s", "forwardUrl": "%s"}' % (status_code, message, callback_type, url)
        return res

# 增加题目
@manage.route("/manage/question_add", endpoint="question_add", methods=["GET", "POST"])
@check_login
@check_is_admin
def question_add():
    if request.method == "GET":
        return render_template("manage_question_add.html")
    else:
        try:
            content = {
                "description": request.form["description"],
                "answer": request.form["answer"],
                "answerA": request.form["answerA"],
                "answerB": request.form["answerB"],
                "answerC": request.form["answerC"],
                "answerD": request.form["answerD"],
            }
            new_question = Qeustions(**content)
            db.session.add(new_question)
            db.session.flush()
            db.session.commit()

            # 将添加的题目加入到redis中
            new_question = new_question.format()
            r.hset("question[%s]" % new_question["id"], "description", new_question["description"])
            r.hset("question[%s]" % new_question["id"], "answerA", new_question["answerA"])
            r.hset("question[%s]" % new_question["id"], "answerB", new_question["answerB"])
            r.hset("question[%s]" % new_question["id"], "answerC", new_question["answerC"])
            r.hset("question[%s]" % new_question["id"], "answerD", new_question["answerD"])
            r.hset("question[%s]" % new_question["id"], "answer", new_question["answer"])
            r.sadd("all_question_id", new_question["id"])
            all_q_nums = len(r.smembers("all_question_id"))
            if all_q_nums < current_app.config["once_exam_nums"]:  # 如果题目池中的题目小于当前设置的题目数
                current_app.config["once_exam_nums"] = all_q_nums
                current_app.config['total_score'] = current_app.config['once_exam_nums'] * current_app.config['one_question_score']   # 总分值
                match = MatchInfo.query.first()
                match.once_exam_nums = current_app.config["once_exam_nums"]
                db.session.commit()

            status_code = 200
            message = "添加成功"
        except:
            status_code = 300
            message = "操作失败"
        callback_type = "forward"
        url = url_for("manage.question_add")
        res = '{"statusCode": %s,"message": "%s", "callbackType": "%s", "forwardUrl": "%s"}' % (status_code, message, callback_type, url)
        return res

# 删除题目
@manage.route("/manage/question_del", endpoint="question_del", methods=["POST"])
@check_login
@check_is_admin
def question_del():
    try:
        del_id = int(request.form.get("del_id"))
        q_del = Qeustions.query.filter_by(id=del_id).first()
        db.session.delete(q_del)
        db.session.commit()
        r.srem("all_question_id", del_id)
        r.delete('question[%s]' % del_id)
        all_q_nums = len(r.smembers("all_question_id"))
        if all_q_nums < current_app.config["once_exam_nums"]:  # 如果题目池中的题目小于当前设置的题目数
            current_app.config["once_exam_nums"] = all_q_nums
            current_app.config['total_score'] = current_app.config['once_exam_nums'] * current_app.config['one_question_score']  # 总分值
            match = MatchInfo.query.first()
            match.once_exam_nums = current_app.config["once_exam_nums"]
            db.session.commit()

        status_code = 200
        message = "删除成功"
    except:
        status_code = 300
        message = "操作失败"
    callback_type = "forward"
    url = url_for("manage.question_libs")
    res = '{"statusCode": %s,"message": "%s", "callbackType": "%s", "forwardUrl": "%s"}' % (status_code, message, callback_type, url)
    return res

# 修改题目
@manage.route("/manage/question_modify", endpoint="question_modify", methods=["GET", "POST"])
@check_login
@check_is_admin
def question_modify():
    if request.method == "POST":
        try:
            search_q_id = int(request.form.get("search_id"))
            search_q_res = Qeustions.query.filter_by(id=search_q_id).first()
            if search_q_res:
                return render_template("manage_question_modify.html", q_search=search_q_res.format())
            else:
                return render_template("manage_question_modify.html")
        except:
            try:
                q = Qeustions.query.filter_by(id=request.form["id"]).first()
                q.id = request.form["id"]
                q.description = request.form["description"]
                q.answer = request.form["answer"]
                q.answerA = request.form["answerA"]
                q.answerB = request.form["answerB"]
                q.answerC = request.form["answerC"]
                q.answerD = request.form["answerD"]
                db.session.commit()
                status_code = 200
                message = "修改成功"
            except:
                status_code = 300
                message = "操作失败"
            callback_type = "forward"
            url = url_for("manage.question_modify")
            res = '{"statusCode": %s,"message": "%s", "callbackType": "%s", "forwardUrl": "%s"}' % (status_code, message, callback_type, url)
            return res
    else:
        return render_template("manage_question_modify.html")

# 题库
@manage.route("/manage/question_libs", endpoint="question_libs", methods=["GET", "POST"])
@check_login
@check_is_admin
def questions():
    if request.method == "GET":
        try:
            now_page = abs(int(request.args.get("page")))
            if now_page == 0:
                now_page = 1
        except:
            now_page = 1
        begin = (now_page - 1) * 10
        result = Qeustions.query.order_by(Qeustions.id).limit(10).offset(begin).all()
        q_display = []
        for i in result:
            q_tmp = {
                "description": i.description,
                "id": i.id
            }
            q_display.append(q_tmp)
        page_nums = ceil(Qeustions.query.count()/10)
        data = {
            "q_display": q_display,
            "page_nums": page_nums,
            "now_page": now_page
        }
        return render_template("manage_question_libs.html", **data)
    else:
        try:
            search_q_id = int(request.form.get("search_q_id"))
            search_q = Qeustions.query.filter_by(id=search_q_id).first()
            if search_q:
                q_display = [{"description": search_q.description, "id": search_q.id}]
            else:
                q_display = []
            data = {
                "q_display": q_display,
                "page_nums": 1,
                "now_page": 1
            }
            return render_template("manage_question_libs.html", **data)
        except:
            try:
                search_q_keywords = request.form.get("search_q_keywords")
                search_q = Qeustions.query.filter(Qeustions.description.like("%{}%".format(search_q_keywords))).all()
                search_q_display = []
                for i in search_q:
                    q_tmp = {
                        "description": i.description,
                        "id": i.id
                    }
                    search_q_display.append(q_tmp)
                page_nums = ceil(len(search_q) / 10)
                data = {
                    "q_display": search_q_display,
                    "page_nums": page_nums,
                    "now_page": 1
                }
                return render_template("manage_question_libs.html", **data)
            except:
                return redirect(url_for("manage.question.libs"))

# 清空数据
@manage.route("/manage/clear_data", endpoint="clear_data", methods=["GET", "POST"])
@check_login
@check_is_admin
def clear_data():
    if request.method == "POST":
        callback_type = "forward"
        url = url_for("manage.clear_data")

        if "del_match_info" in request.form.keys():
            try:
                for match in MatchInfo.query.all():
                    db.session.delete(match)
                db.session.add(MatchInfo())
                db.session.commit()
            except:
                status_code = 300
                message = "删除比赛信息失败"
                res = '{"statusCode": %s,"message": "%s","callbackType": "%s","forwardUrl": "%s"}' % (status_code, message, callback_type, url)
                return res
        if "del_all_user_data" in request.form.keys():
            try:
                users = Users.query.all()
                for user in users:
                    name = user.username
                    r.delete("user:" + name)
                    r.delete("user_question_id:" + name)
                for score in Score.query.all():
                    db.session.delete(score)
                db.session.commit()
            except:
                    status_code = 300
                    message = "删除用户信息失败"
                    res = '{"statusCode": %s,"message": "%s","callbackType": "%s","forwardUrl": "%s"}' % (
                    status_code, message, callback_type, url)
                    return res
        if "del_all_question" in request.form.keys():
            try:
                for q in Qeustions.query.all():
                    db.session.delete(q)
                all_questions_id = r.smembers("all_question_id")
                for q_id in all_questions_id:
                    r.delete("question[%s]" % q_id)
                r.delete("all_question_id")
                db.session.commit()
            except:
                status_code = 300
                message = "删除所有题目失败"
                res = '{"statusCode": %s,"message": "%s","callbackType": "%s","forwardUrl": "%s"}' % (status_code, message, callback_type, url)
                return res
        if "del_all_user" in request.form.keys():
            try:
                for user in Users.query.all():
                    if user.username == "admin":
                        continue
                    db.session.delete(user)
                db.session.commit()
            except:
                status_code = 300
                message = "删除所有用户失败"
                res = '{"statusCode": %s,"message": "%s","callbackType": "%s","forwardUrl": "%s"}' % (status_code, message, callback_type, url)
                return res

        load_questions()
        load_match_info()

        status_code = 200
        message = "清除完成"
        res = '{"statusCode": %s,"message": "%s","callbackType": "%s","forwardUrl": "%s"}' % (status_code, message, callback_type, url)
        return res
    else:
        return render_template("manage_clear_data.html")

# 用户管理
@manage.route("/manage/user_manage", endpoint="user_manage", methods=["GET", "POST"])
@check_login
@check_is_admin
def user_manage():
    if request.method == "GET":
        try:
            now_page = abs(int(request.args.get("page")))
            if now_page == 0:
                now_page = 1
        except:
            now_page = 1
        begin = (now_page - 1) * 10
        result = Users.query.order_by(Users.id).limit(10).offset(begin).all()
        u_display = []
        for i in result:
            u_tmp = {
                "id": i.id,
                "username": i.username,
                "email": i.email or '',
                "password": i.password
            }
            u_display.append(u_tmp)
        page_nums = ceil(Users.query.count()/10)
        data = {
            "u_display": u_display,
            "page_nums": page_nums,
            "now_page": now_page
        }
        return render_template("manage_user_manage.html", **data)
    else:
        callback_type = "forward"
        url = url_for("manage.user_manage")
        if "action" in request.form.keys():
            if request.form["action"] == "modify":
                try:
                    modify_user = Users.query.filter_by(id=int(request.form["modify_id"])).first()
                    if "modify_username" in request.form.keys() and request.form["modify_username"].strip() != "":
                        modify_user.username = request.form["modify_username"]
                    if "modify_email" in request.form.keys() and request.form["modify_email"].strip() != "":
                        modify_user.email = request.form["modify_email"]
                    if "modify_password" in request.form.keys() and request.form["modify_password"].strip() != "":
                        modify_user.password = request.form["modify_password"]
                    db.session.commit()
                    status_code = 200
                    message = "修改成功"
                except:
                    status_code = 300
                    message = "修改失败"
                res = '{"statusCode": %s,"message": "%s","callbackType": "%s","forwardUrl": "%s"}' % (status_code, message, callback_type, url)
                return res

            elif request.form["action"] == "delete":
                try:
                    del_user = Users.query.filter_by(id=int(request.form["del_id"])).first()
                    del_user_name = del_user.username
                    if del_user_name != "admin":
                        r.delete("user:" + del_user_name)
                        r.delete("user_question_id:" + del_user_name)
                        user_score = Score.query.filter_by(username=del_user_name).first()
                        db.session.delete(user_score)
                        db.session.delete(del_user)
                        db.session.commit()

                        status_code = 200
                        message = "删除成功"
                    else:
                        status_code = 300
                        message = "不能删除管理员"
                except:
                    status_code = 300
                    message = "删除失败"
                res = '{"statusCode": %s,"message": "%s","callbackType": "%s","forwardUrl": "%s"}' % (status_code, message, callback_type, url)
                return res

            elif request.form["action"] == "search":
                u_display = []
                search_filter = Users.id == -1      # 没有搜索结果
                if "search_u_email" in request.form.keys() and request.form["search_u_email"] != "":
                    search_u_email = request.form["search_u_email"]
                    search_filter = Users.email.like("%{}%".format(search_u_email))
                elif "search_u_name" in request.form.keys():
                    search_u_name = request.form.get("search_u_name")
                    search_filter = Users.username.like("%{}%".format(search_u_name))

                search_u = Users.query.filter(search_filter).order_by(Users.id).all()
                for i in search_u:
                    u_tmp = {
                        "id": i.id,
                        "username": i.username,
                        "email": i.email,
                        "password": i.password
                    }
                    u_display.append(u_tmp)
                page_nums = ceil(len(search_u) / 10)
                data = {
                    "u_display": u_display,
                    "page_nums": page_nums,
                    "now_page": 1
                }
                return render_template("manage_user_manage.html", **data)

            elif request.form["action"] == "add":
                try:
                    add_username = request.form["add_u_name"]
                    add_email = request.form["add_u_email"]
                    add_password = request.form["add_u_password"]
                    add_user = Users(username=add_username, password=add_password, email=add_email)
                    db.session.add(add_user)
                    db.session.commit()

                    status_code = 200
                    message = "添加成功"
                except:
                    status_code = 300
                    message = "添加失败"
                res = '{"statusCode": %s,"message": "%s","callbackType": "%s","forwardUrl": "%s"}' % (status_code, message, callback_type, url)
                return res

        return "{status_code:200}"
