from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware
from .middleware import *
import os
import sys
from .services import *


def all_general_settings(page):
    try:
        all_user = AddGeneralSettingModel.objects.all()
        paginator = Paginator(all_user, 10)
        contacts = paginator.get_page(page)
        return all_general_settings_data(contacts), contacts.paginator.page_range, None
    except Exception as e:
        logger.error(e)
        return None, None, e


@api_view(['GET', 'POST'])
@decorator_from_middleware(CreateLogoFavIconMiddleware)
def create_logo_fav_icon_view(request, page=1):
    lastid = last_id_logo_fav_icon()
    try:
        if request.method == "POST":
            postdata = [i for i in request.POST.keys()]
            postdata.extend([i for i in request.FILES.keys()])
            print(postdata)
            keyset = set()
            for l in postdata:
                keyset.add(l[0: -1].split("[")[0])
            keyset = list(keyset)
            allkeys = []
            for ks in keyset:
                samekeys = []
                for lst in postdata:
                    if ks in lst:
                        samekeys.append(lst)
                allkeys.append(samekeys)
            for postkey in allkeys:
                if postkey[5] in request.FILES:
                    CreateFavLgoService.execute({
                        "slug": request.POST.get(postkey[0]),
                        "title": request.POST.get(postkey[1]),
                        "field_type": request.POST.get(postkey[2]),
                        "manager": request.POST.get(postkey[3]),
                        "favlogo_value": request.POST.get(postkey[4]),
                        "userid": request.COOKIES['id']
                    }, {"config_value_file": request.FILES[postkey[5]]})
                else:

                    CreateFavLgoService.execute({
                        "slug": request.POST.get(postkey[0]),
                        "title": request.POST.get(postkey[1]),
                        "field_type": request.POST.get(postkey[2]),
                        "manager": request.POST.get(postkey[3]),
                        "favlogo_value": request.POST.get(postkey[4]),
                        "userid": request.COOKIES['id']
                    })
            all_lfv_data = all_logo_fav_icon(page)
            if all_lfv_data[2] is None:
                return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                     "logo_fav_icon": all_lfv_data[0], "last_LFI_id": lastid}, status=200)
            else:
                return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                     "LFV_Error": all_lfv_data[2], "last_LFI_id": lastid}, status=400)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        all_lfv_data = all_logo_fav_icon(page)
        if all_lfv_data[2] is None:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "logo_fav_icon": all_lfv_data[0], "last_LFI_id": lastid, "Error": e}, status=200)
        else:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "LFV_Error": all_lfv_data[2], "last_LFI_id": lastid, "Error": e}, status=400)


@api_view(['GET', 'POST'])
@decorator_from_middleware(DeleteLogoFavIconMiddleware)
def delete_logo_fav_icon_view(request, icon_id, page=1):
    lastid = last_id_logo_fav_icon()
    try:
        LogoFavIconsModel.objects.get(id=icon_id).delete()
        all_lfv_data = all_logo_fav_icon(page)
        if all_lfv_data[2] is None:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "logo_fav_icon": all_lfv_data[0], "last_LFI_id": lastid}, status=200)
        else:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "LFV_Error": all_lfv_data[2], "last_LFI_id": lastid}, status=400)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        all_lfv_data = all_logo_fav_icon(page)
        if all_lfv_data[2] is None:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "logo_fav_icon": all_lfv_data[0], "last_LFI_id": lastid,
                                 "Error": str((e, exc_type, f_name, exc_tb.tb_lineno))}, status=200)
        else:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "LFV_Error": all_lfv_data[2], "last_LFI_id": lastid,
                                 "Error": str((e, exc_type, f_name, exc_tb.tb_lineno))}, status=400)


@api_view(['GET', 'POST'])
@decorator_from_middleware(GeneralSettingMiddleware)
def create_general_settings_view(request, form):
    try:
        CreateGenSettingService.execute({
            "title": form.cleaned_data.get("title"),
            "Constant_Slug": form.cleaned_data.get("Constant_Slug"),
            "field_type": form.cleaned_data.get("field_type"),
            "config_value": form.cleaned_data.get("config_value"),
            "userid": request.COOKIES['id']
        })
        return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id']))}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                             "Error": str((e, exc_type, f_name, exc_tb.tb_lineno))}, status=400)


@api_view(['GET', 'POST'])
def get_general_settings_view(request, page=1):
    try:
        all_gs_data = all_general_settings(page)
        if all_gs_data[2] is None:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                "general_settings": all_gs_data[0]}, status=200)
        else:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                "general_settings": all_gs_data[0],
                                 "GS_Error": all_gs_data[2]}, status=400)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        all_gs_data = all_general_settings(page)
        if all_gs_data[2] is None:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "general_settings": all_gs_data[0],
                                 "Error": str((e, exc_type, f_name, exc_tb.tb_lineno))}, status=200)
        else:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "general_settings": all_gs_data[0],
                                 "Error": str((e, exc_type, f_name, exc_tb.tb_lineno)),
                                 "GS_Error": all_gs_data[2]}, status=400)


@api_view(['GET', 'POST'])
@decorator_from_middleware(ViewGeneralSettingMiddleware)
def view_general_settings_view(request, gs_id):
    try:
        return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                             "general_settings": general_settings_data(AddGeneralSettingModel.objects.get(id=gs_id))},
                            status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                             "Error": str((e, exc_type, f_name, exc_tb.tb_lineno))}, status=400)


@api_view(['GET', 'POST'])
@decorator_from_middleware(ViewGeneralSettingMiddleware)
def delete_general_settings_view(request, gs_id, page=1):
    try:
        AddGeneralSettingModel.objects.get(id=gs_id).delete()
        all_gs_data = all_general_settings(page)
        if all_gs_data[2] is None:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                "general_settings": all_gs_data[0]}, status=200)
        else:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                "general_settings": all_gs_data[0],
                                 "GS_Error": all_gs_data[2]}, status=400)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        all_gs_data = all_general_settings(page)
        if all_gs_data[2] is None:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "general_settings": all_gs_data[0],
                                 "Error": str((e, exc_type, f_name, exc_tb.tb_lineno))}, status=200)
        else:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "general_settings": all_gs_data[0],
                                 "Error": str((e, exc_type, f_name, exc_tb.tb_lineno)),
                                 "GS_Error": all_gs_data[2]}, status=400)


@api_view(['GET', 'POST'])
@decorator_from_middleware(ViewGeneralSettingMiddleware)
def edit_general_settings_view(request, form, gs_id):
    try:
        if request.method == "POST":
            EditGenSettingService.execute({
                "title": form.cleaned_data.get("title"),
                "Constant_Slug": form.cleaned_data.get("Constant_Slug"),
                "field_type": form.cleaned_data.get("field_type"),
                "config_value": form.cleaned_data.get("config_value"),
                "gs_id": gs_id
            })
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "general_settings": general_settings_data(AddGeneralSettingModel.objects.get(id=gs_id))},
                                status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                             "Error": str((e, exc_type, f_name, exc_tb.tb_lineno))}, status=400)


@api_view(['GET', 'POST'])
@decorator_from_middleware(SMTPDeatilsMiddleware)
def smtp_detail_view(request, form):
    if request.method == "POST":
        try:
            SMTPDetailService.execute({
                "SMTP_ALLOW": form.cleaned_data.get("SMTP_ALLOW"),
                "SMTP_EMAIL": form.cleaned_data.get("SMTP_EMAIL"),
                "SMTPPASSWORD": form.cleaned_data.get("SMTPPASSWORD"),
                "SMTPPORT": form.cleaned_data.get("SMTPPORT"),
                "SMTPUSERNAME": form.cleaned_data.get("SMTPUSERNAME"),
                "SMTP_TLS": form.cleaned_data.get("SMTP_TLS"),
                "userid": request.COOKIES['id']
            })
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "smtpdata": all_smtp_data(SMTPDetailModel.objects.get())})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "smtpdata": all_smtp_data(SMTPDetailModel.objects.get()),
                                 "Error": str((e, exc_type, f_name, exc_tb.tb_lineno))}, status=400)


@api_view(['GET', 'POST'])
@decorator_from_middleware(AddSocialURLsMiddleware)
def add_social_urls_view(request, form, page=1):
    last_id = last_id_social_url()
    try:
        if request.method == "POST":
            requestdata = form.cleaned_data
            title = eval(requestdata['title'])
            field_type = eval(requestdata['field_type'])
            manager = eval(requestdata['manager'])
            url = eval(requestdata['url'])
            icon = eval(requestdata['icon'])
            social_value = eval(requestdata["social_value"])
            if len(title) == len(field_type) == len(manager) == len(url) == len(icon) == len(social_value):
                for i in range(len(title)):
                    SocialURLsService.execute({
                        "userid": request.COOKIES['id'],
                        "title": title[i],
                        "social_value": social_value[i],
                        "url": url[i],
                        "iconclass": icon[i],
                        "field_type": field_type[i],
                        "manager": manager[i]
                    })
                allsocialurls = all_social_urls(page)
                if allsocialurls[2] is None:
                    return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                         "all_social_urls": allsocialurls[0],
                                         "social_urls_last_id": last_id}, status=200)
                else:
                    return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                         "social_data_error": allsocialurls[2]}, status=400)
            else:
                allsocialurls = all_social_urls(page)
                if allsocialurls[2] is None:
                    return JsonResponse(
                        {"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                         "all_social_urls": allsocialurls[0],
                         "social_attribute_error": "Attribute are missing please provide all attribute of all fields",
                         "social_urls_last_id": last_id}, status=200)
                else:
                    return JsonResponse(
                        {"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                         "social_attribute_error": "Attribute are missing please provide all attribute of all fields",
                         "social_data_error": allsocialurls[2]}, status=400)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        allsocialurls = all_social_urls(page)
        if allsocialurls[2] is None:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "all_social_urls": allsocialurls[0],
                                 "Error": str((e, exc_type, f_name, exc_tb.tb_lineno)),
                                 "social_urls_last_id": last_id}, status=200)
        else:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "Error": str((e, exc_type, f_name, exc_tb.tb_lineno)),
                                 "social_data_error": allsocialurls[2],
                                 "social_urls_last_id": last_id}, status=400)


@api_view(['GET', 'POST'])
@decorator_from_middleware(DeleteSocialURLsMiddleware)
def delete_social_urls_view(request, su_id, page=1):
    last_id = last_id_social_url()
    try:
        SocialURLsModel.objects.get(id=su_id).delete()
        allsocialurls = all_social_urls(page)
        if allsocialurls[2] is None:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "all_social_urls": allsocialurls[0],
                                 "social_urls_last_id": last_id}, status=200)
        else:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "social_data_error": allsocialurls[2]}, status=400)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
        allsocialurls = all_social_urls(page)
        if allsocialurls[2] is None:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "all_social_urls": allsocialurls[0],
                                 "social_urls_last_id": last_id,
                                 "Error": str((e, exc_type, f_name, exc_tb.tb_lineno)),}, status=200)
        else:
            return JsonResponse({"UserData": UserInfo(User.objects.get(account_id=request.COOKIES['id'])),
                                 "Error": str((e, exc_type, f_name, exc_tb.tb_lineno)),
                                 "social_urls_last_id": last_id,
                                 "social_data_error": allsocialurls[2]}, status=400)
