import os
import sys
import requests

# from query_mysql import get_users_login_info
from flask_login import UserMixin, LoginManager
from urllib.parse import urljoin

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import configs.config as config

login_manager = LoginManager()
login_manager.login_view = "login"


class User(UserMixin):
    def is_admin(self):
        return self.admin

    def is_super_admin(self):
        return self.super_admin


@login_manager.user_loader
def user_loader(user_name):
    users = get_users()
    if user_name not in users:
        return

    user = User()
    user.id = user_name
    user.member_id = users[user_name]["member_id"]
    user.admin = users[user_name]["is_admin"]
    user.super_admin = users[user_name]["is_super_admin"]
    return user


@login_manager.request_loader
def request_loader(request):
    user_name = request.form.get("user_name")
    users = get_users()
    if user_name not in users:
        return

    user = User()
    user.id = user_name
    return user


def get_users():
    members = requests.get(urljoin(config.HOST, "/api/members")).json()
    return {member["user_name"]: member for member in members}
