from flask import Flask, g
from flask_themes2 import Themes, get_theme, render_theme_template
from flask_login   import LoginManager, UserMixin
from funcs.login import login_bp
from funcs.page import page_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'
Themes(app, app_identifier="your_project")

# Login Logic Handling
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


def get_current_theme():
    return get_theme('default')

@app.route('/')
def index():
    return render_theme_template(get_current_theme(), 'index.html')

app.register_blueprint(login_bp)
app.register_blueprint(page_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
