from django.contrib import admin
from django.urls import path, re_path

from cat import views

urlpatterns = [
    path('admin_panel/', views.admin_panel),
    path('admin/', admin.site.urls),
    path('', views.index),
    path('parsing/', views.my_view),
    path('providers/create/', views.create_provider),
    path('providers/<int:id>/delete/', views.delete_provider),
    path('providers/<int:id>/', views.update_prov),
    path('providers/', views.all_providers),
    path('unknows/<int:title>/del_yes', views.del_unk),
    path('unknows/_<int:page>/is_del', views.is_del_all_unknown),
    path('unknows/_<int:page>/del', views.del_all_unknown),
    path('unknows/_<int:page>/', views.all_unk_prods),
    path('unknows/<int:title>/', views.unk_page_prod),
    re_path(r'^prods/_(?P<page>\d+)/$', views.all_prods),
    path('prods/<str:title>/upd', views.update_prod),
    path('prods/<str:title>/del_yes', views.del_agreed),
    path('prods/<str:title>/del', views.del_prod),
    path('prods/<str:title>/', views.page_prod),
    path('reg/', views.reg, name='register'),
    path('login/change', views.change_pass),
    path('login/', views.login_page),
    path('history/', views.history),
    path('user/', views.user_page),
    path('load/', views.load_prices)


]
