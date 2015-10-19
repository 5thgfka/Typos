#-*- coding: utf-8 -*-
'''
Created on 2015-08-04

@author: ekse
'''
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson 
from typos.models import *

import hashlib
import datetime

def home(request):
    template_var = {}
    # new
    typos_list_new = Typos.objects.filter(status = 0)[:6]
    # confirm
    typos_list_confirm = Typos.objects.filter(status = 1)[:6]
    
    template_var['typos_list_confirm'] = typos_list_confirm
    template_var['typos_list_new'] = typos_list_new
    
    return render_to_response("index.html",template_var, context_instance=RequestContext(request))


def contact(request):
    template_var = {}
    return render_to_response("contacts.html",template_var, context_instance=RequestContext(request))


def submit_typos(request):

    template_var = {}
    if request.method.upper() == 'GET':
        return render_to_response("submit.html",template_var, context_instance=RequestContext(request))
    else:
        corpName = request.POST['corpName']
        link = request.POST['link']
        inWord = request.POST['inWord']
        inCentence = request.POST['inCentence']
        correctWord = request.POST['correctWord']
        # convert to md5
        typos_hash = hashlib.md5(inCentence.encode('utf-8')).hexdigest()
        status = 0
        typos = Typos()
        # 
        if not request.user.is_authenticated():
            publisher = User.objects.get(id=1)
        else:
            publisher = request.user
        corp = Corp.objects.get(name = corpName)

        typos.phrases = inWord
        typos.sentence = inCentence
        typos.correct_phrases = correctWord
        typos.url = link
        typos.publisher = publisher
        typos.typos_hash = typos_hash
        typos.status = status
        typos.belongto = corp
        typos.submit_time = "%s" % datetime.date.today()

        typos.save()
        template_var["status"] = "success"
        
        return HttpResponse(simplejson.dumps(template_var, ensure_ascii = False), content_type="application/json")


def typo(request, typoid):
    template_var = {}

    typo = Typos.objects.get(id = typoid)

    template_var['phrases'] = typo.phrases
    template_var['sentence'] = typo.sentence
    template_var['error_url'] = typo.url
    template_var['submit_time'] = typo.submit_time
    template_var['publisher'] = typo.publisher
    template_var['audit_time'] = typo.audit_time
    template_var['typos_hash'] = typo.typos_hash
    template_var['status'] = typo.status

    return render_to_response("typo.html",template_var, context_instance=RequestContext(request))

def user(request, userid):
    template_var = {}
    
    typos = Typos.objects.filter(publisher = userid)
    userObj = User.objects.get(id = userid)

    name = userObj.username

    template_var['name'] = name

    typos_0 = [typo for typo in typos if typo.status == '0']
    typos_1 = [typo for typo in typos if typo.status == '1']

    typos_0_count = len(typos_0)
    typos_1_count = len(typos_1)

    template_var['unConfirmed'] = typos_0_count
    template_var['confirmed'] = typos_1_count

    template_var['typos_0'] = typos_0
    template_var['typos_1'] = typos_1
    
    return render_to_response("user.html",template_var, context_instance=RequestContext(request))
