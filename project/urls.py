from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('registration/', views.registration, name='registration'),
    path('account_created_successfully/', views.account_created_successfully, name='account_created_successfully'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my_account/', views.my_account, name='my_account'),
    path('report_found_item/', views.report_found_item, name='report_found_item'),
    path('report_lost_item/', views.report_lost_item, name='report_lost_item'),
    path('search_lost_item/', views.search_lost_item, name='search_lost_item'),
    path('manage_report/', views.manage_report, name='manage_report'),
    path('logout/', views.logout, name='logout'),
    path('edit_lost_item/<int:item_id>/', views.edit_lost_item, name='edit_lost_item'),
    path('edit_found_item/<int:item_id>/', views.edit_found_item, name='edit_found_item'),
    path('delete-item/', views.delete_item, name='delete-item'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)