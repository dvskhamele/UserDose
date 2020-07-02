from django.urls import path
from .views import UserExistsViewSet, CSVViewSet, UserViewSet, UserLoginViewSet, LogoutView, UserCreateView


app_name = "Users"

urlpatterns = [
    # User list
    path('', UserViewSet.as_view(),name='user_list'),
    path(r'register', UserCreateView.as_view(), name='register'),
    # User list to a csv
    path('user_list_in_csv/', CSVViewSet.as_view(), name='user_list_in_csv'),
    # Check id user already have an account
    path('check_if_user_exists/', UserExistsViewSet.as_view(), name='check_if_user_exists'),
    path('login/',UserLoginViewSet.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),


]
