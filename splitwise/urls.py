from django.urls import path

from splitwise.views import *

urlpatterns = [
    path('test', AddTransactionView.as_view(), name='testview'),
    path('create_user', CreateUserView.as_view(), name='create_user'),
    path('user_balance/<int:user_id>', UserExpenseView.as_view(), name='create_user'),
    path('user_balances', UserBalances.as_view(), name='create_user'),
]