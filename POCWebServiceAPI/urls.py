"""POCWebServiceAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from UserAPI.views import *
from secondaryDB.views import *
from settings.views import *
from email_template.views import *
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/pages/', user_table),
    path('api/v1/users/pages/<int:page>/', user_table),
    path('api/v1/users/pages/add/', admin_user_view),
    path('api/v1/users/pages/edit/<int:user_id>/', edit_user_data),
    path('api/v1/users/pages/view/<int:user_id>/', view_user),
    path('api/v1/users/pages/delete/<int:user_id>/', delete_user),
    path('api/v1/users/login/', user_login),
    path('api/v1/users/logout/', user_logout_view),
    path('api/v1/cms-manager/pages/', cms_page_view),
    path('api/v1/cms-manager/pages/<int:page>/', cms_page_view),
    path('api/v1/cms-manager/pages/add/', create_cms_page_view),
    path('api/v1/cms-manager/pages/edit/<int:cms_id>/', edit_cms_page_view),
    path('api/v1/cms-manager/pages/view/<int:cms_id>/', view_cms_page_view),
    path('api/v1/cms-manager/pages/delete/<int:cms_id>/', delete_cms_page_view),
    path('api/v1/email-manager/email-hooks/add/', create_email_hook_view),
    path('api/v1/email-manager/email-hooks/add/<int:page>', create_email_hook_view),
    path("api/v1/setting-manager/settings/smtp/", smtp_detail_view),
    path("api/v1/setting-manager/settings/social/", add_social_urls_view),
    path("api/v1/setting-manager/settings/social/<int:page>/", add_social_urls_view),
    path("api/v1/setting-manager/settings/social/delete/<int:su_id>/", delete_social_urls_view),
    path('api/v1/setting-manager/settings/', get_general_settings_view),
    path('api/v1/setting-manager/settings/<int:page>/', get_general_settings_view),
    path('api/v1/setting-manager/settings/add/', create_general_settings_view),
    path('api/v1/setting-manager/settings/view/<int:gs_id>/', view_general_settings_view),
    path('api/v1/setting-manager/settings/delete/<int:gs_id>/', delete_general_settings_view),
    path('api/v1/setting-manager/settings/edit/<int:gs_id>/', edit_general_settings_view),
    path('api/v1/setting-manager/settings/logos/', create_logo_fav_icon_view),
    path('api/v1/setting-manager/settings/logos/<int:page>/', create_logo_fav_icon_view),
    path('api/v1/setting-manager/settings/logos/delete/<int:icon_id>/', delete_logo_fav_icon_view),
]

if not settings.DEBUG:
    urlpatterns += [
                    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
                    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
                    ]

# handler404 = 'adminapp.views.view_404'
# handler500 = 'adminapp.views.view_500'

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
