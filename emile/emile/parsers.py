from .models import User
import json


def user_from_json(user_json_string):
    user_dict = json.loads(user_json_string)
    user = User(phone=user_dict['phone'], currentPlan=user_dict['currentPlan'], personalInfo=user_dict['personalInfo'])
    return user


