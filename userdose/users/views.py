import csv
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import    APIView
from rest_framework.viewsets import GenericViewSet
from .serializers import UserSerializer, CreateUserSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.generic import TemplateView
from django.shortcuts import render 
from django.contrib.auth import authenticate, login
from rest_framework import status


User = get_user_model()

class UserViewSet(TemplateView):
    """
    Updates and retrieves user accounts
    """
    template_name = "users/list.html"
    permission_classes = (AllowAny,)

    def get_context_data(self, *args, **kwargs):
        context = super(UserViewSet, self).get_context_data(*args, **kwargs)
        context['users'] = User.objects.exclude(email="")
        return context

class UserCreateViewSet(CreateModelMixin,
                        GenericViewSet,
                        TemplateView):
    """
    Creates user accounts
    """
    template_name = "users/registration.html"
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        new_user = authenticate(email=request.POST.get('email'),
            password=request.POST.get('password'),
            )
        if new_user is not None:
            if new_user.is_active:
                django_login(request, new_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserExistsViewSet(APIView):
    """
    Checks User's Existance
    """
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        # if username is being sent as a query parameter
        username = self.request.query_params.get('username')

        users = User.objects.all().values() # retrieve the user using username
        try:
            if username == None:
                # if email is being sent as a query parameter
                email = self.request.query_params.get('email')
                user = User.objects.get(email=email) # retrieve the user using username
            else:
                user = User.objects.get(username=username) # retrieve the user using username
        except User.DoesNotExist:
            return Response(data={'message':False}) # return false as user does not exist
        except:
            pass
        return Response(data={'message':True,
        'error_message':"The user with this details is already taken, Lets try another one?"}) # Otherwise, return True

class CSVViewSet(APIView):
    """
    Outputs a CSV File of UserList
    """
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.DictWriter(response, fieldnames=['Label', 'Value',])
        writer.writeheader()
        # use this if username is in url kwargs
        usernames = self.kwargs.get('usernames')
        print("usernames",usernames)
        if usernames == None:
            usernames = self.request.query_params.getlist('username')
        print("usernames",usernames)
        if usernames == None:
            users = User.objects.all()
        else:
            users = User.objects.filter(username__in=usernames)
        for user in users:
            if user.username != "" or user.email != "" :
                writer.writerow({'Label': user.username, 'Value': user.email})
        return response

