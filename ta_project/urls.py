"""
URL configuration for ta_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from ta_app.views.Home import Home
from ta_app.views.courseList import courseList
from ta_app.views.accountList import accountList
from ta_app.views.accountView import accountView
from ta_app.views.loginView import login_view
from django.views.generic.base import RedirectView
from ta_app.views.SectionView import SectionView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Home/',Home.as_view(),name='Home'),
    path('Home/courseList/',courseList.as_view(),name="courseList"),
    path('Home/createSection/',SectionView.as_view(),name="createSection"),
    path('Home/accountList/',accountList.as_view(),name="accountList"),
    path('Home/accountList/<int:pk>/',accountView.as_view(),name="accountDetails"),
    path('login/', login_view.as_view(), name='login'),
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
]

