from exts import app, r
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class Qeustions(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    description = db.Column(db.TEXT)
    answerA = db.Column(db.TEXT)
    answerB = db.Column(db.TEXT)
    answerC = db.Column(db.TEXT)
    answerD = db.Column(db.TEXT)
    answer = db.Column(db.VARCHAR(11))

    def format(self):
        return dict(id=self.id, description=self.description, answerA=self.answerA, answerB=self.answerB, answerC=self.answerC, answerD=self.answerD, answer=self.answer)


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(20), unique=True)
    email = db.Column(db.VARCHAR(30), unique=True, default="")
    password = db.Column(db.VARCHAR(50))
    is_admin = db.Column(db.INT, default=0)

    def format(self):
        return dict(id=self.id, username=self.username, email=self.email, password=self.password, is_admin=self.is_admin)


class Score(db.Model):
    __tablename__ = "score"
    username = db.Column(db.VARCHAR(20), primary_key=True)
    score = db.Column(db.INT)
    start_time = db.Column(db.VARCHAR(30))
    finish_time = db.Column(db.VARCHAR(30))
    spend_time = db.Column(db.INT)

    def format(self):
        return dict(username=self.username, score=self.score, start_time=self.start_time, finish_time=self.finish_time, spend_time=self.spend_time)


class MatchInfo(db.Model):
    __tablename__ = "match_info"
    match_name = db.Column(db.VARCHAR(30), primary_key=True, default="")
    match_start_time = db.Column(db.VARCHAR(30), default="0")
    match_end_time = db.Column(db.VARCHAR(30), default="0")
    match_duration = db.Column(db.INT, default=0)
    one_question_score = db.Column(db.INT, default=0)
    once_exam_nums = db.Column(db.INT, default=0)

    def format(self):
        res = {
            "match_name": self.match_name,
            "match_start_time": self.match_start_time,
            "match_end_time": self.match_end_time,
            "match_duration": self.match_duration,
            "one_question_score": self.one_question_score,
            "once_exam_nums": self.once_exam_nums
        }
        return res


# 从数据库加载比赛信息
def load_match_info():
    match = MatchInfo.query.first().format()
    app.config["match_name"] = match.get("match_name")
    app.config["match_start_time"] = match.get("match_start_time").replace("T", " ") + ":00"
    app.config["match_end_time"] = match.get("match_end_time").replace("T", " ") + ":00"
    app.config["match_duration"] = abs(int(match.get("match_duration")))
    app.config["one_question_score"] = abs(int(match.get("one_question_score")))
    app.config["once_exam_nums"] = abs(int(match.get("once_exam_nums")))
    app.config['total_score'] = app.config['once_exam_nums'] * app.config['one_question_score']   # 总分值


# 将所有题目从数据库取出，放进redis中
def load_questions():
    questions = Qeustions.query.order_by(Qeustions.id).all()  # 查询所有题目
    for question in questions:                                # 放入redis
        question_dit = question.format()
        r.hset("question[%s]" % question_dit["id"], "description", question_dit["description"])
        r.hset("question[%s]" % question_dit["id"], "answerA", question_dit["answerA"])
        r.hset("question[%s]" % question_dit["id"], "answerB", question_dit["answerB"])
        r.hset("question[%s]" % question_dit["id"], "answerC", question_dit["answerC"])
        r.hset("question[%s]" % question_dit["id"], "answerD", question_dit["answerD"])
        r.hset("question[%s]" % question_dit["id"], "answer", question_dit["answer"])
        r.sadd("all_question_id", question_dit["id"])


load_match_info()
load_questions()

if __name__ == '__main__':
    score_data = {
        "username": 1,
        "score": 2,
        "finish_time": 3,
        "start_time": 4,
        "spend_time": 5
    }
    a =Score(**score_data)
    print(a.score)


