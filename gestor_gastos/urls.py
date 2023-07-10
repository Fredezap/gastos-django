from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movementsIndex/', views.movementsIndex, name='movementsIndex'),
    path('movementsCreate/', views.movementsCreate, name='movementsCreate'),
    path('categoriesIndex/', views.categoriesIndex, name='categoriesIndex'),
    path('categoriesIndex/<letter>/', views.categoriesIndex, name='categoriesIndex'),
    path('categoriesCreate/', views.categoriesCreate, name='categoriesCreate'),
    path('fundsIndex/', views.fundsIndex, name='fundsIndex'),
    path('fundsMovementCreate/', views.fundsMovementCreate, name='fundsMovementCreate'),
    path('savingsDeposit/<int:id>', views.savingsDeposit, name='savingsDeposit'),
    path('savingsWithdraw/<int:id>', views.savingsWithdraw, name='savingsWithdraw'),
    path('movementsMonthly/', views.movementsMonthly, name='movementsMonthly'),
    path('redistributeLeftoverMoney/', views.redistributeLeftoverMoney, name='redistributeLeftoverMoney'),
    path('redistributeLeftoverMoney/<str:current_funds>', views.redistributeLeftoverMoney, name='redistributeLeftoverMoney'),
]