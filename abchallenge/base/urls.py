from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('accounts/', views.accounts, name='accounts'),
    path('transactions/', views.transactions, name='transactions'),
    path('repayments/', views.repayments, name='repayments'),
    path('reports/', views.reports, name='reports'),
    path('perform-advance/', views.performAdvance, name='perform-advance'),
    path('myaccount/', views.myaccount, name='myaccount'),
]