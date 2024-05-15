from django.views import View
from django.shortcuts import render, redirect
from ta_app.models import Course
from django.contrib import messages


class removeCourseAssignment(View):
    def get(self, request, user_pk, course_pk):
        pass

    def post(self, request, user_pk, course_pk):
        pass