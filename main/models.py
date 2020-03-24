# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Algorithm(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=4096)
    owner = models.PositiveIntegerField()
