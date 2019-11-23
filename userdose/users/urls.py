from django.urls import path
from .views import UserExistsViewSet, CSVViewSet, UserViewSet

app_name = "Users"

urlpatterns = [
    # User list
    path('', UserViewSet.as_view()),
    # User list to a csv
    path('user_list_in_csv/', CSVViewSet.as_view()),
    # Check id user already have an account
    path('check_if_exists/', UserExistsViewSet.as_view()),
]
