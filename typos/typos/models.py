#-*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Corp(models.Model):
	name = models.CharField(max_length = 20, null=True, verbose_name = "公司")

class Typos(models.Model):
	phrases = models.CharField(max_length = 20, null=True, verbose_name = "所在词组")
	sentence = models.CharField(max_length = 1000, null=True, verbose_name = "所在句子")
	correct_phrases = models.CharField(max_length = 1000, null=True, verbose_name = "正确词组")
	url = models.CharField(max_length = 100, verbose_name = "链接")
	belongto = models.ForeignKey(Corp, verbose_name = "公司")
	submit_time = models.DateField(verbose_name = "提交时间")
	publisher = models.ForeignKey(User, verbose_name = "提交人")
	audit_time = models.DateField(verbose_name = "审核时间", null=True)
	typos_hash = models.CharField(max_length = 1000, null=True, verbose_name = "句子HASH")
	status = models.CharField(max_length = 10, verbose_name="状态")

admin.site.register(Corp)
admin.site.register(Typos)
