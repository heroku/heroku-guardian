from heroku_guardian.utils import utils
import json


def get_user_info():
    user_info = json.loads(utils.heroku_auth(f"account").get_heroku_api())
    return user_info