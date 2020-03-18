from exts import app
from flask import render_template
from user import user
from display import display
from exam import exam
from manage import manage

app.register_blueprint(user)
app.register_blueprint(display)
app.register_blueprint(exam)
app.register_blueprint(manage)


@app.errorhandler(405)
def error_405(error):
    return render_template("405.html"), 405


@app.errorhandler(404)
def error_404(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def error_500(error):
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
