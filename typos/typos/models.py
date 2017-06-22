#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Corp(models.Model):
	name = models.CharField(max_length = 20, null=True, verbose_name = "公司")
	
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "公司名称"
		verbose_name_plural = "公司名称"

class Typos(models.Model):
	'''
	v1:
	@summary:
		1.belongto为外键关联Corp
	v2:
	@date:2016-02-01
	@summary:
		1.修改belongto为CharField
	'''
	phrases = models.CharField(max_length = 20, null=True, verbose_name = "所在词组")
	sentence = models.CharField(max_length = 1000, null=True, verbose_name = "所在句子")
	correct_phrases = models.CharField(max_length = 1000, null=True, verbose_name = "正确词组")
	url = models.CharField(max_length = 100, verbose_name = "链接")
	#belongto = models.ForeignKey(Corp, verbose_name = "公司")
	belongto = models.CharField(max_length = 100, verbose_name = "公司")
	submit_time = models.DateField(verbose_name = "提交时间")
	publisher = models.ForeignKey(User, verbose_name = "提交人")
	audit_time = models.DateField(verbose_name = "审核时间", null=True)
	typos_hash = models.CharField(max_length = 1000, null=True, verbose_name = "句子HASH")
	status = models.CharField(max_length = 10, verbose_name="状态")

	def __unicode__(self):
		return self.phrases

	class Meta:
		verbose_name = "别字"
		verbose_name_plural = "别字"

class Apply(models.Model):
	email = models.CharField(max_length = 40, verbose_name = "email")
	applyDate = models.DateField(verbose_name = "申请日期")
	replyDate = models.DateField(verbose_name = "反馈日期")

	def __unicode__(self):
		return self.email

	class Meta:
		verbose_name = "用户申请"
		verbose_name_plural = "用户申请"

class Test(models.Model):
	published = models.BooleanField(default=False)
