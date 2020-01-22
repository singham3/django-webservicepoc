from django.utils.deprecation import MiddlewareMixin
from .forms import *
from POCWebServiceAPI.admininfo import *
from POCWebServiceAPI.hashers import *
from .models import *
from django.http import HttpResponse, JsonResponse
import os
import sys
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from .allsettingsdata import *


def last_id_logo_fav_icon():
    if LogoFavIconsModel.objects.count() == 1:
        lastdata = LogoFavIconsModel.objects.get()
        lastid = int(lastdata.favlogo_value.split("_favlogo_value")[0]) + 1
    elif LogoFavIconsModel.objects.count() == 0:
        lastid = 1
    else:
        lastdata = LogoFavIconsModel.objects.last()
        lastid = int(lastdata.favlogo_value.split("_favlogo_value")[0]) + 1
    return lastid


def last_id_social_url():
    if SocialURLsModel.objects.count() == 1:
        lastdata = SocialURLsModel.objects.get()
        lastid = int(lastdata.social_value.split("_socialvalue")[0]) + 1
    elif SocialURLsModel.objects.count() == 0:
        lastid = 1
    else:
        lastdata = SocialURLsModel.objects.last()
        lastid = int(lastdata.social_value.split("_socialvalue")[0]) + 1
    return lastid


def all_social_urls(page):
    try:
        all_user = SocialURLsModel.objects.all()
        paginator = Paginator(all_user, 10)
        contacts = paginator.get_page(page)
        return all_social_urls_data(contacts), contacts.paginator.page_range, None
    except Exception as e:
        logger.error(e)
        return None, None, e


def all_logo_fav_icon(page):
    try:
        all_user = LogoFavIconsModel.objects.all()
        paginator = Paginator(all_user, 10)
        contacts = paginator.get_page(page)
        return all_logo_fav_icon_data(contacts), contacts.paginator.page_range, None
    except Exception as e:
        logger.error(e)
        return None, None, e


class CreateLogoFavIconMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            return None
        lastid = last_id_logo_fav_icon()
        all_lfv_data = all_logo_fav_icon(1)
        if all_lfv_data[2] is None:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "logo_fav_icon": all_lfv_data[0], "last_LFI_id": lastid}, status=200)
        else:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "LFV_Error": all_lfv_data[2], "last_LFI_id": lastid}, status=400)

    def process_response(self, request, response):
        return response


class DeleteLogoFavIconMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if 'icon_id' in view_kwargs and view_kwargs['icon_id']:
                if LogoFavIconsModel.objects.filter(id=view_kwargs['icon_id']).exists():
                    return None

                else:
                    return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                         "Error": "Id {} Not Exist In logos Pages".format(view_kwargs['icon_id'])},
                                        status=404)
            else:
                return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                     "Error": "URL Not Correct!! Please Provide Valid logos Page Id"},
                                    status=404)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))

    def process_response(self, request, response):
        return response


class GeneralSettingMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = GeneralSettingForm(request.POST, request.FILES)
            if not form.is_valid():
                if form.errors:
                    logger.error(form.errors)
                    return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                         "form_error": form.errors}, status=400)
                if form.non_field_errors:
                    logger.error(form.non_field_errors)
                    return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                         "form_error": form.non_field_errors}, status=400)
            else:
                return view_func(request, form)

    def process_response(self, request, response):
        return response


class ViewGeneralSettingMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'gs_id' in view_kwargs and view_kwargs['gs_id']:
            if AddGeneralSettingModel.objects.filter(id=view_kwargs['gs_id']).exists():
                if request.method == "POST":
                    form = GeneralSettingForm(request.POST, request.FILES)
                    if not form.is_valid():
                        if form.errors:
                            logger.error(form.errors)
                            return JsonResponse(
                                {"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "form_error": form.errors}, status=400)
                        if form.non_field_errors:
                            logger.error(form.non_field_errors)
                            return JsonResponse(
                                {"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "form_error": form.non_field_errors}, status=400)
                    else:
                        return view_func(request, form, view_kwargs['gs_id'])
                return None
            else:
                return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                     "Error": "Id {} Not Exist In General Setting Pages".format(view_kwargs['gs_id'])},
                                    status=404)
        else:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "Error": "URL Not Correct!! Please Provide Valid General Setting Page Id"},
                                status=404)

    def process_response(self, request, response):
        return response


class SMTPDeatilsMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = SMTPDetailForm(request.POST)
            if not form.is_valid():
                if form.errors:
                    logger.error(form.errors)
                    return JsonResponse(
                        {"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                         "form_error": form.errors}, status=400)
                if form.non_field_errors:
                    logger.error(form.non_field_errors)
                    return JsonResponse(
                        {"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                         "form_error": form.non_field_errors}, status=400)
            else:
                return view_func(request, form)
        return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                            "smtpdata": all_smtp_data(SMTPDetailModel.objects.get())})

    def process_response(self, request, response):
        return response


class AddSocialURLsMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = SocialURLsForm(request.POST, request.FILES)
            if not form.is_valid():
                if form.errors:
                    logger.error(form.errors)
                    return JsonResponse(
                        {"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                         "form_error": form.errors}, status=400)
                if form.non_field_errors:
                    logger.error(form.non_field_errors)
                    return JsonResponse(
                        {"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                         "form_error": form.non_field_errors}, status=400)
            else:
                return view_func(request, form)
        last_id = last_id_social_url()
        allsocialurls = all_social_urls(1)
        if allsocialurls[2] is None:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "all_social_urls": allsocialurls[0],
                                 "social_urls_last_id": last_id}, status=200)
        else:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "social_data_error": allsocialurls[2]}, status=400)
    
    def process_response(self, request, response):
        return response


class DeleteSocialURLsMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'su_id' in view_kwargs and view_kwargs['su_id']:
            if SocialURLsModel.objects.filter(id=view_kwargs['su_id']).exists():
                return None
            else:
                return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                     "Error": "Id {} Not Exist In Social URLs Pages".format(view_kwargs['su_id'])},
                                    status=404)
        else:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "Error": "URL Not Correct!! Please Provide Valid Social URLs Page Id"},
                                status=404)

    def process_response(self, request, response):
        return response
