from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('', views.home, name='home'),
    path('account_create/', views.account_create, name='account_create'),
    path('pin_generation',views.pin_generation,name='pin_generation'),
    path('deposite',views.deposite,name='deposite'),
    path('with/',views.withdraw,name='withdraw'),
    path('transfer_money',views.transfer_money,name='tansfer_money'),
    path('account_details',views.account_details,name='account_details'),
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)