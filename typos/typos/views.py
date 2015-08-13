#-*- coding: utf-8 -*-
'''
Created on 2015-08-04

@author: ekse
'''
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render_to_response
from django.template import RequestContext
from typos.models import *

import hashlib
import datetime

def home(request):
    template_var = {}
    # new
    typos_list_new = Typos.objects.all()[:6]
    # confirm
    typos_list_confirm = Typos.objects.filter(status = 1)
    
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

        return HttpResponse(template_var)
