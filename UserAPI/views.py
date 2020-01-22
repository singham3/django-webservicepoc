from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import decorator_from_middleware
from .middleware import *
from random import randint
from ipware import get_client_ip
from .services import *
from django.contrib import auth
import jwt
from datetime import datetime, timedelta
from collections import OrderedDict
from django.core.paginator import Paginator
import os
import sys


def all_users(page):
    try:
        all_user = User.objects.all()
        paginator = Paginator(all_user, 10)
        contacts = paginator.get_page(page)
        return contacts, contacts.paginator.page_range, None
    except Exception as e:
        logger.error(e)
        return None, None, e


@decorator_from_middleware(AllUserMiddleware)
def user_table(request, page=1):
    try:
        all_users_data = all_users(page)
        all_user_data = []
        for i in all_users_data[0]:
            all_user_data.append(UserInfo(i))
        return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])), 
                             "AllUserData": all_user_data, "Error": all_users_data[2]}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return JsonResponse({"Error": str((e, exc_type, f_name, exc_tb.tb_lineno)), "UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id']))},
                            status=500)


@api_view(['GET', 'POST'])
@decorator_from_middleware(AddUserMiddleware)
def admin_user_view(request, form):
    if request.method == "POST":
        try:
            CreateUserService.execute({
                'username': form.cleaned_data.get('username'),
                'first_name': form.cleaned_data.get('first_name'),
                'last_name': form.cleaned_data.get('last_name'),
                'email': form.cleaned_data.get('email'),
                'mobile': form.cleaned_data.get('mobile'),
                'password': form.cleaned_data.get('password'),
                'date_of_birth': form.cleaned_data.get('date_of_birth'),
                'status': form.cleaned_data.get('status'),
                'browser_type': request.META['HTTP_USER_AGENT'],
                'user_ip': get_client_ip(request)[0],
                'account_id': randint(10 ** (8 - 1), (10 ** 8) - 1)
                }, {'user_img': form.cleaned_data.get('user_img')})
            user_data = User.objects.get(username=form.cleaned_data.get('username'), 
                                         email=form.cleaned_data.get('email'))
            return JsonResponse({"UserData": UserInfo(user_data)}, status=200)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            return JsonResponse({"Error": str((e, exc_type, f_name, exc_tb.tb_lineno)), 
                                 "UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id']))}, status=500)


@api_view(['GET', 'POST'])
@decorator_from_middleware(EditUserMiddleware)
def edit_user_data(request, form, user_id):
    if request.method == "POST":
        try:
            EditUserService.execute({
                "username": form.cleaned_data.get('username'),
                "first_name": form.cleaned_data.get('first_name'),
                "last_name": form.cleaned_data.get("last_name"),
                "mobile": form.cleaned_data.get("mobile"),
                "account_id": user_id,
                "date_of_birth": form.cleaned_data.get("date_of_birth"),
                "email": form.cleaned_data.get("email"),
                "status": int(form.cleaned_data.get("status")),
                "browser_type": request.META['HTTP_USER_AGENT'],
                "user_ip": get_client_ip(request)[0],
            }, {"user_img": form.cleaned_data.get("user_img")})
            logger.info("{} Successfully Updated".format(form.cleaned_data.get("email")))
            user_data = User.objects.get(account_id=user_id)
            return JsonResponse({"msg": ugettext("Successfully Updated"), "UserData": UserInfo(user_data)}, status=200)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            user_data = User.objects.get(account_id=user_id)
            return JsonResponse({"Error": str((e, exc_type, f_name, exc_tb.tb_lineno)), 
                                 "UserData": UserInfo(user_data)}, status=500)


@api_view(['GET', 'POST'])
@decorator_from_middleware(ViewUserMiddleware)
def view_user(request, user_id):
    try:
        user_data = User.objects.get(account_id=user_id)
        return JsonResponse({"UserData": UserInfo(user_data)}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return JsonResponse({"Error": str((e, exc_type, f_name, exc_tb.tb_lineno)), 
                             "UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id']))}, status=500)


@api_view(['GET', 'POST'])
@decorator_from_middleware(ViewUserMiddleware)
def delete_user(request, user_id):
    try:
        user_data = User.objects.db_manager('default').get(account_id=user_id)
        if User.objects.get(account_id=request.COOKIES['id']) != user_data:
            delete_user_var = UserInfo(user_data)
            user_data.delete()
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])), 
                                 "DeleteUser": delete_user_var}, status=200)
        else:
            return JsonResponse({"Error": "User not permission to delete"}, status=500)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return JsonResponse({"Error": str((e, exc_type, f_name, exc_tb.tb_lineno)),
                             "UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id']))}, status=500)


@api_view(['GET', 'POST'])
@decorator_from_middleware(LoginMiddleware)
def user_login(request, form):
    if request.method == "POST":
        try:
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            browser_type = request.META['HTTP_USER_AGENT']
            user_ip = get_client_ip(request)[0]
            if User.objects.filter(email=email).exists():
                user_data = User.objects.get(email=email)
                user = authenticate(username=user_data.username, password=password)
                if user is not None:

                    token = jwt.encode({
                        'account_id': user_data.account_id,
                        'username': user_data.username,
                        'email': user_data.email,
                        'token_created_at': str(datetime.now()),
                        'a': {2: True},
                        'exp': datetime.utcnow() + timedelta(seconds=86400)},
                        token_key["token_key"],
                        algorithm='HS256'
                    )
                    user_data.token = token.decode()
                    user_data.loginBrowser = browser_type
                    user_data.loginip = user_ip
                    user_data.last_login = datetime.now()
                    user_data.key = None
                    user_data.save()
                    return JsonResponse({'token': token.decode(), "msg": "Successfully Login",
                                         "UserData": UserInfo(user_data)}, status=200)
                else:
                    return JsonResponse({"Error": 'Incorrect username and password'}, status=400)
            else:
                return JsonResponse({"Error": 'Invalid Username and Password'}, status=400)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            return JsonResponse({"Error": str((e, exc_type, f_name, exc_tb.tb_lineno))}, status=500)


@api_view(['GET', 'POST'])
def user_logout_view(request):
    try:
        user_data = User.objects.get(account_id=request.COOKIES['id'])
        user_data.token = None
        user_data.save()
        request.COOKIES.pop('id')
        return JsonResponse({'message': "{} Successfully Logout".format(user_data.username)}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return JsonResponse({"Error": str((e, exc_type, f_name, exc_tb.tb_lineno))}, status=500)
