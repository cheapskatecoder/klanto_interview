from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.urls import reverse


class Dashboard(View):
    template_name = "portal/dashboard.html"

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        else:
            return HttpResponseRedirect('signup')


class Signin(View):
    template_name = 'portal/signin.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('portal:dashboard'))
            else:
                messages.error(request, 'Either Username or Password is incorrect', extra_tags='alert alert-danger')
                return HttpResponseRedirect(reverse('portal:signin'))
        else:
            messages.error(request, 'Username and Password both are required', extra_tags='alert alert-danger')
            return HttpResponseRedirect(reverse('portal:signin'))


class Signup(View):
    template_name = 'portal/signup.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        print(request.POST)

        if username and password and email:
            user = User.objects.create(username=username, password=password, email=email)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('portal:dashboard'))
        else:
            message.error(request, 'All the fields are required', extra_tags='alert alert-danger')
            return HttpResponseRedirect(reverse('portal:signup'))


class Portfolio(View):
    template_name = 'portal/portfolio.html'

    def get(self, request):
        return render(request, self.template_name, context={'file': 'https://drive.google.com/file/d/1oGhhJUDozo4fbtmg9W4nnad2jJ5yX5Je/view?usp=sharing'})