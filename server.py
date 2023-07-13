from exam_app import app

from exam_app.controllers import users_controller, tv_shows_controller
# ...server.py

if __name__ == "__main__":
    app.run(debug = True, port = 5001)