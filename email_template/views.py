from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware
from .middleware import *
import os
import sys
from .services import *


@api_view(['GET', 'POST'])
@decorator_from_middleware(CreateEmailHookMiddleware)
def create_email_hook_view(request, form, page=1):
    try:
        if request.method == "POST":
            CreateEmailHookService.execute({
                "title": form.cleaned_data.get("title"),
                "hook": form.cleaned_data.get("hook"),
                "description": form.cleaned_data.get("description"),
                "status": int(form.cleaned_data.get("status")),
                "userid": request.COOKIES['id'],
            })
        allemailhoo = all_email_hook(page)
        if allemailhoo[2] is None:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "all_email_hook_data": allemailhoo[0]}, status=200)
        else:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "email_hook_error": allemailhoo[2]}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                             "Error": str((e, exc_type, f_name, exc_tb.tb_lineno))}, status=500)
