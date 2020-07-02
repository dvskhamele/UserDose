import csv
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from django.urls import reverse
from rest_framework.views import    APIView
from rest_framework.viewsets import GenericViewSet
from .serializers import UserSerializer, CreateUserSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import views as auth_views
from django.shortcuts import resolve_url
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q






User = get_user_model()
@method_decorator(login_required, name='dispatch')
class UserViewSet(TemplateView):
    """
    Updates and retrieves user accounts
    """
    template_name = "users/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(UserViewSet, self).get_context_data(*args, **kwargs)
        context['users'] = User.objects.exclude(email="")
        context['username'] = self.request.user
        return context

class UserCreateViewSet(CreateModelMixin,
                        GenericViewSet,
                       ):
    """
    Creates user accounts
    """
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        new_user = authenticate(username=request.POST.get('username'),
            password=request.POST.get('password'),
            )
        print("request.POST.get('email')",request.POST.get('email'))
        print("request.POST.get('password')",request.POST.get('password'))
        if new_user is None:
            new_user = authenticate(username=request.POST.get('username'),
            password=request.POST.get('password'),
            )
            print('new_user1',new_user)
        if new_user is not None:
            if new_user.is_active:
                print('new_user',new_user)
                login(request, new_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserCreateView(
                        TemplateView):
    template_name = "users/registration.html"

class UserExistsViewSet(APIView):
    """
    Checks User's Existance
    """
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        # if username is being sent as a query parameter
        username = self.request.query_params.get('username')
        print('username',username)
        users = User.objects.all().values() # retrieve the user using username
        try:
            user = User.objects.get(Q(email=username) | Q(username=username)) # retrieve the user using username
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








class UserLoginViewSet(TemplateView):
    template_name = 'account/login.html'
    def post(self, request):
        context={}
        username = request.POST['username']
        password = request.POST['password']
        print('username',username)
        print('password',password)
        user = authenticate(username=username, password=password)
        if user is None:
            user = authenticate_user(username,password)
        print('user',user)
        if user is not None:
            if user.is_active:
                print('inside if')
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                print('inside if after login')
                return HttpResponseRedirect(reverse('products:product_list'))
            else:
                context['error_message'] = "user is not active"
        else:
            context['error_message'] = "Email or password not correct"
            print("context['error_message']",context['error_message'])
            return render(request,'account/login.html',context)

def authenticate_user(username, password):
    UserModel = get_user_model()
    print('hello i am in')
    try:
        user = UserModel.objects.get(email=username)
    except UserModel.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user
    return None



class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('users:login'))
