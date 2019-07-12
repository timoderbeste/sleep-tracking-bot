from flask import Blueprint

main = Blueprint('main', __name__)

from . import user_views, record_views, datum_views, update_user, plan_views, admin_view, function
