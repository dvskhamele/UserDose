from django.urls import path
from .views import UserExistsViewSet, CSVViewSet

app_name = "Users"

urlpatterns = [
    # Check id user already have an account
    path('check_if_exists/', UserExistsViewSet.as_view()),
     # User list in a csv
   path('user_list_in_csv/', CSVViewSet.as_view()),
]