# -*- coding: utf-8 -*-
from django.conf.urls import url
from handgesturerecognition.myapp.views import imageUpload

urlpatterns = [
    url(r'^imageUpload/$', imageUpload, name='imageUpload')
]
