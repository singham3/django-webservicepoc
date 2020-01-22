from django.utils.translation import ugettext
import logging

logging.basicConfig(filename="debug/debug.log",
                    format='%(asctime)s %(name)-15s %(levelname)-5s %(message)s : [%(pathname)s line %(lineno)d, in %(funcName)s ]',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def UserInfo(model_object):
    return {
        "id": model_object.id,
        'username': model_object.username,
        'email': model_object.email,
        "is_email": bool(model_object.isemail),
        "first_name": model_object.first_name,
        "last_name": model_object.last_name,
        "user_img": model_object.userimg.url,
        'date_of_birth': model_object.dateofbirth.strftime('%m/%d/%Y'),
        'date_joined': model_object.date_joined.strftime('%m/%d/%Y %H:%M:%S.%I'),
        "updated_at": model_object.updatedat.strftime('%m/%d/%Y %H:%M:%S.%I'),
        "account_id": model_object.account_id,
        'mobile': model_object.mobile, "is_mobile": bool(model_object.ismobile),
        "status": True if bool(model_object.is_superuser) and bool(model_object.is_staff) and bool(model_object.is_active) else False
    }