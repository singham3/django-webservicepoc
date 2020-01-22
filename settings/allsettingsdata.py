from .models import *
from POCWebServiceAPI.hashers import *
import base64


def all_logo_fav_icon_data(alfi_obj):
    all_logo_fav_icon_list = []
    for i in alfi_obj:
        all_logo_fav_icon_list.append({
            'id': i.id,
            'slug': i.slug,
            'title': i.title,
            'field_type': i.field_type,
            'manager': i.manager,
            'favlogo_value': i.favlogo_value,
            'config_value_file': i.config_value_file.url,
            'created_at': i.createdat.strftime('%m/%d/%Y %H:%M:%S.%I'),
            'updated_at': i.updatedat.strftime('%m/%d/%Y %H:%M:%S.%I'),
            'username': i.userid.username
        })
    return all_logo_fav_icon_list


def all_general_settings_data(gs_obj):
    all_general_settings_list = []
    for i in gs_obj:
        all_general_settings_list.append({
            'id': i.id,
            'title': i.title,
            'Constant_Slug': i.Constant_Slug,
            'field_type': i.field_type,
            'config_value_bool': i.config_value_bool,
            'config_value_text': i.config_value_text,
            'created_at': i.createdat.strftime('%m/%d/%Y %H:%M:%S.%I'),
            'updated_at': i.updatedat.strftime('%m/%d/%Y %H:%M:%S.%I'),
            'username': i.userid.username
        })
    return all_general_settings_list


def general_settings_data(gs_obj):
    return {
        'id': gs_obj.id,
        'title': gs_obj.title,
        'Constant_Slug': gs_obj.Constant_Slug,
        'field_type': gs_obj.field_type,
        'config_value_bool': gs_obj.config_value_bool,
        'config_value_text': gs_obj.config_value_text,
        'created_at': gs_obj.createdat.strftime('%m/%d/%Y %H:%M:%S.%I'),
        'updated_at': gs_obj.updatedat.strftime('%m/%d/%Y %H:%M:%S.%I'),
        'username': gs_obj.userid.username
    }


def all_smtp_data(smtp_obj):
    return {
        'SMTP_EMAIL': smtp_obj.SMTP_EMAIL,
        'SMTPPASSWORD': base64.b64encode(decrypt_message_rsa(smtp_obj.SMTPPASSWORD, jsondata["privatekey"]).encode()).decode(),
        'SMTPPORT': smtp_obj.SMTPPORT,
        'SMTPUSERNAME': smtp_obj.SMTPUSERNAME,
        'SMTP_ALLOW': smtp_obj.SMTP_ALLOW,
        'SMTPTLS': smtp_obj.SMTPTLS,
        'created_at': smtp_obj.createdat.strftime('%m/%d/%Y %H:%M:%S.%I'),
        'updated_at': smtp_obj.updatedat.strftime('%m/%d/%Y %H:%M:%S.%I'),
        'username': smtp_obj.userid.username
    }


def all_social_urls_data(su_obj):
    all_social_urls_list = []
    for i in su_obj:
        all_social_urls_list.append({
            'id': i.id,
            'username': i.userid.username,
            'title': i.title,
            'social_value': i.social_value,
            'url': i.url,
            'icon_class': i.icon_class,
            'field_type': i.field_type,
            'manager': i.manager,
            'create_at': i.createat.strftime('%m/%d/%Y %H:%M:%S.%I'),
            'update_at': i.updateat.strftime('%m/%d/%Y %H:%M:%S.%I')
        })
    return all_social_urls_list
