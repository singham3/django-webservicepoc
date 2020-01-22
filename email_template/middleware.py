from django.utils.deprecation import MiddlewareMixin
from .forms import *
from POCWebServiceAPI.admininfo import *
from .allemailtemplate import *
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
import os
import sys
from datetime import datetime, timedelta


def all_email_hook(page):
    try:
        all_user = AddEmailHooksModel.objects.all()
        paginator = Paginator(all_user, 10)
        contacts = paginator.get_page(page)
        return all_email_hook_data(contacts), contacts.paginator.page_range, None
    except Exception as e:
        logger.error(e)
        return None, None, e


class CreateEmailHookMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = AddEmailHookForm(request.POST)
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
                return view_func(request, form, view_kwargs['page'])
        else:
            print(view_kwargs['page'])
            allemailhoo = all_email_hook(view_kwargs['page'])
            if allemailhoo[2] is None:
                return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                     "all_email_hook_data": allemailhoo[0]}, status=200)
            else:
                return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                     "email_hook_error": allemailhoo[2]}, status=200)

    def process_response(self, request, response):
        return response
