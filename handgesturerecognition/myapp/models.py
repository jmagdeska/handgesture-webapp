# -*- coding: utf-8 -*-
from django.db import models

class Image(models.Model):
    image = models.FileField(upload_to='images/')

