from django.urls import path
from .views import RegisterView, LoginView, RegisterAdminView, UserCreateView, MyAgentView,MyLegalMemberView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/admin', RegisterAdminView.as_view(), name='register_admin'),
    path('create-user/', UserCreateView.as_view(), name='create-user'),
    path('agents-view/', MyAgentView.as_view(), name='agents-view'),
    path('legal-view/', MyLegalMemberView.as_view(), name='legal-view'),
]
