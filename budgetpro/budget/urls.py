from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]

from django.urls import path
from . import views

urlpatterns += [
    path('add/', views.add_transaction, name='add_transaction'),
    path('chart-data/', views.transaction_chart_data, name='transaction_chart_data'),
]

urlpatterns += [
    path('', views.dashboard, name='dashboard'),
    path('chart-data/', views.expense_chart_data, name='expense_chart_data'), 
]
