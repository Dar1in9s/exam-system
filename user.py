from flask import Blueprint, session, redirect, url_for, request, render_template
from module import Users
from sqlalchemy import and_, or_
user = Blueprint("user", __name__)

# 登录
@user.route("/login", endpoint="login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        try:      # 判断是否已经登陆过了
            test = session["user"]
            if session["is_admin"]:
                return redirect(url_for("manage.match_info"))
            else:
                return redirect(url_for("exam.exam"))
        except:
            return render_template("login.html")
    else:
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            filter_login = and_(Users.password == password, or_(Users.email == username, Users.username == username))
            user_login = Users.query.filter(filter_login).first()
            if user_login:
                session['user'] = user_login.username
                session["is_admin"] = user_login.is_admin

                status_code = 200
                message = "登录成功"
                callback_type = "forward"
                if session["is_admin"]:
                    url = url_for("manage.match_info")
                else:
                    url = url_for("exam.exam")

                res = '{"statusCode": %s,"message": "%s","callbackType": "%s","forwardUrl": "%s"}' % (status_code, message, callback_type, url)
            else:
                status_code = 300
                message = "用户名或密码错误"
                res = '{"statusCode": %s,"message": "%s"}' % (status_code, message)
            return res
        except:
            return render_template("login.html")

# 注销
@user.route("/logout", endpoint="logout")
def logout():
    session.clear()
    return redirect(url_for("user.login"))

