from django.urls import path

from splitwise.views import *

urlpatterns = [
    path('add_transaction', AddTransactionView.as_view(), name='add_transaction'),
    path('create_user', CreateUserView.as_view(), name='create_user'),
    path('user_balance/<int:user_id>', UserExpenseView.as_view(), name='create_user'),
    path('user_balances', UserBalances.as_view(), name='create_user'),
]