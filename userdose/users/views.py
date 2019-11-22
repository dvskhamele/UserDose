import csv
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from .serializers import UserSerializer, CreateUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

User = get_user_model()

class UserViewSet(ListModelMixin,
                  GenericViewSet,
                  ):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class UserCreateViewSet(CreateModelMixin,
                        GenericViewSet):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)

class UserExistsViewSet(APIView):
    """
    Checks User's Existance
    """
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        # use this if username is in url kwargs
        username = self.kwargs.get('username') 

        # use this if username is being sent as a query parameter
        username = self.request.query_params.get('username')  

        try:
            user = User.objects.get(Q(username=username)|Q(email=username)) # retrieve the user using username
        except User.DoesNotExist:
            return Response(data={'message':False}) # return false as user does not exist
        else:
            return Response(data={'message':True}) # Otherwise, return True

class CSVViewSet(APIView):
    """
    Outputs a CSV File of UserList
    """

    def get(self, request, format=None):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.DictWriter(response, fieldnames=['Label', 'Value',])
        writer.writeheader()
        for user in User.objects.all():
            if user.username != "" or user.email != "" :
                writer.writerow({'Label': user.username, 'Value': user.email})
        return response

