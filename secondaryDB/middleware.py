from django.utils.deprecation import MiddlewareMixin
from .forms import *
from POCWebServiceAPI.admininfo import *
from django.http import HttpResponse, JsonResponse
from .allcmspages import *
import os
import sys
from datetime import datetime, timedelta


class CreateCMSPageMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.method == "POST":
                if "cms_file" not in request.FILES:
                    logger.error("CMS New Page Add has File Field is required")
                    return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                         "form_error": {"cms_file": ["This field is required."]}},
                                        status=400)
                form = CMSPageForm(request.POST, request.FILES)
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
        except Exception as e:
            logger.error(e)
            return JsonResponse({"Error": e}, status=500)

    def process_response(self, request, response):
        return response


class EditCMSPageMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if 'cms_id' in view_kwargs and view_kwargs['cms_id']:
                if CMSpagemodel.objects.filter(id=view_kwargs['cms_id']).exists():
                    cms_data = CMSpagemodel.objects.get(id=view_kwargs['cms_id'])
                    if request.method == "POST":
                        form = CMSPageForm(request.POST, request.FILES)
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
                            return view_func(request, form, view_kwargs['cms_id'])
                    return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                        "cms_data": cms_pages_data(cms_data)}, status=200)
                else:
                    return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                         "Error": "Id {} Not Exist In CMS Pages".format(view_kwargs['cms_id'])},
                                        status=404)
            else:
                return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                     "Error": "URL Not Correct!! Please Provide Valid CMS Page Id"},
                                    status=404)
        except Exception as e:
            logger.error(e)
            return JsonResponse({"Error": e}, status=500)

    def process_response(self, request, response):
        return response


class ViewCMSPageMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if 'cms_id' in view_kwargs and view_kwargs['cms_id']:
                if CMSpagemodel.objects.filter(id=view_kwargs['cms_id']).exists():
                    return view_func(request, view_kwargs['cms_id'])
                else:
                    return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                         "Error": "Id {} Not Exist In CMS Pages".format(view_kwargs['cms_id'])},
                                        status=404)
            else:
                return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                     "Error": "URL Not Correct Please Provide Valid CMS Page Id"},
                                    status=404)
        except Exception as e:
            logger.error(e)
            return JsonResponse({"Error": e}, status=500)

    def process_response(self, request, response):
        return response