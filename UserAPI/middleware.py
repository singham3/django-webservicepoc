from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from .forms import *
from POCWebServiceAPI.admininfo import *
from django.http import HttpResponse, JsonResponse
from .TokenAuthentigetion import *
import traceback
from django.utils.functional import SimpleLazyObject
import os
import sys
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta

View_class = ['user_login']


class CommonMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if view_func.__name__ not in View_class:
                token_authentication = user_token_authentication(request)
                if token_authentication is None:
                    return JsonResponse({'Error': "Token Not Found"}, status=403)
                elif isinstance(token_authentication, dict):
                    if "Error" in token_authentication:

                        return JsonResponse({'Error': token_authentication['Error']},
                                            status=token_authentication['status'])
                elif token_authentication:
                    request.COOKIES['id'] = token_authentication.account_id
                    if request.method == "POST":
                        return None
                    return None
                else:
                    return JsonResponse({'Error': "Token Authentication Failed"}, status=403)
            else:
                token_authentication = user_token_authentication(request)
                if token_authentication is None:
                    return None
                if isinstance(token_authentication, dict):
                    if "Error" in token_authentication:
                        return JsonResponse({'Error': token_authentication['Error']},
                                            status=token_authentication['status'])
                elif token_authentication:
                    request.session['last_activity'] = str(datetime.now())
                    return JsonResponse({"UserData": UserInfo(token_authentication)}, status=200)
                else:
                    return None
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            return JsonResponse({"Error": str((e, exc_type, f_name, exc_tb.tb_lineno))}, status=500)


class StandardExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        logger.error(exception)
        if User.objects.filter(account_id=request.COOKIES['id']).exists():
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "Error": str(exception)}, status=500)
        return JsonResponse({"Error": exception}, status=500)


class AllUserMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        return None
    
    def process_template_response(self, request, response):
        return response


class AddUserMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.method == "POST":
                form = AddAdminForm(request.POST, request.FILES)
                if not form.is_valid():
                    if form.errors:
                        logger.error(form.errors)
                        return JsonResponse(form.errors, status=400)
                    if form.non_field_errors:
                        logger.error(form.non_field_errors)
                        return JsonResponse(form.non_field_errors, status=400)
                else:
                    return view_func(request, form)
        except Exception as e:
            logger.error(e)
            return JsonResponse({"Error": e}, status=500)

    def process_response(self, request, response):
        return response


class EditUserMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if 'user_id' in view_kwargs and view_kwargs['user_id']:
                if User.objects.filter(account_id=view_kwargs['user_id']).exists():
                    user_data = User.objects.get(account_id=view_kwargs['user_id'])
                    if request.method == "POST":
                        form = EditUserForm(request.POST, request.FILES)
                        if not form.is_valid():
                            if form.errors:
                                logger.error(form.errors)
                                return JsonResponse(form.errors, status=400)
                            if form.non_field_errors:
                                logger.error(form.non_field_errors)
                                return JsonResponse(form.non_field_errors, status=400)
                        else:
                            return view_func(request, form, view_kwargs['user_id'])
                    return JsonResponse({"UserData": UserInfo(user_data)}, status=200)
                else:
                    logger.error("This ID {} Not Found".format(view_kwargs['user_id']))
                    return JsonResponse({"Error": "This ID {} Not Found".format(view_kwargs['user_id'])}, status=404)
            else:
                logger.error("This ID {} Not Found".format(view_kwargs['user_id']))
                return JsonResponse({"Error": "This ID {} Not Found".format(view_kwargs['user_id'])}, status=404)
        except Exception as e:
            logger.error(e)
            return JsonResponse({"Error": e}, status=500)

    def process_response(self, request, response):
        return response


class ViewUserMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if 'user_id' in view_kwargs and view_kwargs['user_id']:
                if User.objects.filter(account_id=view_kwargs['user_id']).exists():
                    return view_func(request, view_kwargs['user_id'])
                else:
                    logger.error("This ID {} Not Found".format(view_kwargs['user_id']))
                    return JsonResponse({"Error": "This ID {} Not Found".format(view_kwargs['user_id'])}, status=404)
            else:
                logger.error("This ID {} Not Found".format(view_kwargs['user_id']))
                return JsonResponse({"Error": "This ID {} Not Found".format(view_kwargs['user_id'])}, status=404)
        except Exception as e:
            logger.error(e)
            return JsonResponse({"Error": e}, status=500)


class LoginMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.method == "POST":
                form = LoginForm(request.POST)
                if not form.is_valid():
                    if form.errors:
                        logger.error(form.errors)
                        return JsonResponse(form.errors)
                    if form.non_field_errors:
                        logger.error(form.non_field_errors)
                        return JsonResponse(form.non_field_errors)
                else:
                    return view_func(request, form)
        except Exception as e:
            logger.error(e)
            return JsonResponse({"Error": e}, status=500)

    def process_template_response(self, request, response):
        return response
