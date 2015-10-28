#encoding=utf8

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout
from django.views.decorators.csrf import csrf_protect
from django import forms
from django.contrib import messages
from accounts.forms import *

from accounts.forms import *
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from typos.models import Apply

import datetime

def login(request):
    '''登陆视图'''
    template_var={}
    form = LoginForm()
    if request.method == 'POST':
        form=LoginForm(request.POST.copy())
        if form.is_valid():
            #print form.cleaned_data["username"],form.cleaned_data["password"]
            _login(request,form.cleaned_data["username"],form.cleaned_data["password"])
            #return render_to_response("index.html",template_var,context_instance=RequestContext(request))
            return HttpResponseRedirect("/")
    template_var["form"]=form
    return render_to_response("registration/login.html",template_var,context_instance=RequestContext(request))

def _login(request,username,password):
    '''登陆核心方法'''
    ret=False
    user=authenticate(username=username,password=password)
    if user:
        if user.is_active:
            auth_login(request,user)
            ret=True
        else:
            messages.add_message(request, messages.INFO, _(u'用户没有激活'))
    else:
        messages.add_message(request, messages.INFO, _(u'用户不存在'))
    return ret

def logout(request):
    '''注销视图'''
    auth_logout(request)
    return HttpResponseRedirect("/")


def register(request):
    '''申请注册'''
    template_var={}
    form = ApplyRegisterForm()
    if request.method.upper() == 'GET':
        template_var["form"]=form
        return render_to_response("registration/register.html",template_var, context_instance=RequestContext(request))
    else:

        form=ApplyRegisterForm(request.POST.copy())
        if form.is_valid():
            email = form.cleaned_data["email"]
            applyDate = "%s" % datetime.date.today()
            replyDate = '2012-02-04'
            tempAp = Apply.objects.filter(email = email)
            # 如果已经申请就不保存了
            if len(tempAp) > 0:
                return HttpResponseRedirect("/")

            ap = Apply()
            ap.email = email
            ap.applyDate = applyDate
            ap.replyDate = replyDate
            ap.save()

        return HttpResponseRedirect("/")
