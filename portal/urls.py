from django.urls import path
from portal import views

app_name = 'portal'

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('signin', views.Signin.as_view(), name='signin'),
    path('signup', views.Signup.as_view(), name='signup'),
    path('portfolio', views.Portfolio.as_view(), name='portfolio'),
    path('railz-redirect', views.RailzRedirect.as_view(), name='railz-redirect')
]

