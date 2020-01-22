from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware
from .middleware import *
import os
import sys
from .services import *
from django.core.paginator import Paginator


def all_cms_pages(page):
    try:
        all_user = CMSpagemodel.objects.all()
        paginator = Paginator(all_user, 10)
        contacts = paginator.get_page(page)
        return contacts, contacts.paginator.page_range, None
    except Exception as e:
        logger.error(e)
        return None, None, e


@api_view(['GET', 'POST'])
def cms_page_view(request, page=1):
    all_cms_page_data = all_cms_pages(page)
    if all_cms_page_data[2] is None:
        return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                             'all_cms_pages_list': all_cms_pages_list(all_cms_page_data[0],)}, status=200)
    else:
        return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                             'Error': all_cms_page_data[2]}, status=400)


@api_view(['GET', 'POST'])
@decorator_from_middleware(CreateCMSPageMiddleware)
def create_cms_page_view(request, form, page=1):
    if request.method == "POST":
        try:
            CreateCMSPageService.execute({
                'title': form.cleaned_data.get('title'),
                'meta_title': form.cleaned_data.get('meta_title'),
                'sub_title': form.cleaned_data.get('sub_title'),
                'meta_keyword': form.cleaned_data.get('meta_keyword'),
                'slug': form.cleaned_data.get('slug'),
                'meta_description': form.cleaned_data.get('meta_description'),
                'short_description': form.cleaned_data.get('short_description'),
                'html_description': form.cleaned_data.get('html_description'),
                'user_id': request.COOKIES['id']
            }, {'cms_file': form.cleaned_data.get('cms_file')})
            all_cms_page_data = all_cms_pages(page)
            if all_cms_page_data[2] is None:
                return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                     'all_cms_pages_list': all_cms_pages_list(all_cms_page_data[0], )}, status=200)
            else:
                return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                     'Error': all_cms_page_data[2]}, status=400)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "Error": str((e, exc_type, f_name, exc_tb.tb_lineno))}, status=500)


@api_view(['GET', 'POST'])
@decorator_from_middleware(EditCMSPageMiddleware)
def edit_cms_page_view(request, form, cms_id):
    if request.method == "POST":
        try:
            EditCMSPageService.execute({
                'title': form.cleaned_data.get('title'),
                'meta_title': form.cleaned_data.get('meta_title'),
                'sub_title': form.cleaned_data.get('sub_title'),
                'meta_keyword': form.cleaned_data.get('meta_keyword'),
                'slug': form.cleaned_data.get('slug'),
                'meta_description': form.cleaned_data.get('meta_description'),
                'short_description': form.cleaned_data.get('short_description'),
                'html_description': form.cleaned_data.get('html_description'),
                'cms_id': cms_id
            }, {'cms_file': form.cleaned_data.get('cms_file')})
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "cms_data": cms_pages_data(CMSpagemodel.objects.get(id=cms_id))},
                                status=200)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "cms_data": cms_pages_data(CMSpagemodel.objects.get(id=cms_id)),
                                 "Error": str((e, exc_type, f_name, exc_tb.tb_lineno))}, status=500)


@api_view(['GET', 'POST'])
@decorator_from_middleware(ViewCMSPageMiddleware)
def view_cms_page_view(request, cms_id):
    try:
        return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                            "cms_data": cms_pages_data(CMSpagemodel.objects.get(id=cms_id))}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return JsonResponse({"UserData": UserInfo(request.user),
                             "cms_data": cms_pages_data(CMSpagemodel.objects.get(id=cms_id)),
                             "Error": str((e, exc_type, f_name, exc_tb.tb_lineno))}, status=500)


@api_view(['GET', 'POST'])
@decorator_from_middleware(ViewCMSPageMiddleware)
def delete_cms_page_view(request, cms_id, page=1):
    try:
        cms_data = CMSpagemodel.objects.get(id=cms_id)
        cms_data.delete()
        all_cms_page_data = all_cms_pages(page)
        if all_cms_page_data[2] is None:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 'all_cms_pages_list': all_cms_pages_list(all_cms_page_data[0])}, status=200)
        else:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 'Error': all_cms_page_data[2]}, status=400)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        all_cms_page_data = all_cms_pages(page)
        if all_cms_page_data[2] is None:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 'all_cms_pages_list': all_cms_pages_list(all_cms_page_data[0]),
                                 "Error": str((e, exc_type, f_name, exc_tb.tb_lineno))}, status=200)
        else:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 'Error': all_cms_page_data[2],
                                 "View_Error": str((e, exc_type, f_name, exc_tb.tb_lineno))}, status=400)
