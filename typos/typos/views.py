#-*- coding: utf-8 -*-
'''
Created on 2017-06-22

@author: ekse
'''
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson 
from typos.models import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

import hashlib
import datetime

import urllib2
import re
from bs4 import BeautifulSoup

def home(request):
    template_var = {}
    # new
    typos_list_comfirmed = Typos.objects.filter(status = 2)[:10]
    # confirm
    typos_list_modified = Typos.objects.filter(status = 3)[:10]
    
    template_var['typos_list_modified'] = typos_list_modified
    template_var['typos_list_comfirmed'] = typos_list_comfirmed
    
    return render_to_response("index.html",template_var, context_instance=RequestContext(request))


def contact(request):
    template_var = {}
    return render_to_response("contacts.html",template_var, context_instance=RequestContext(request))

@login_required
def submit_typos(request):

    template_var = {}
    if request.method.upper() == 'GET':
        return render_to_response("submit.html",template_var, context_instance=RequestContext(request))
    else:

        checkcode_correct = request.session['checkcode']
        checkcode_input = request.POST['checkCode']
        # checkcode verify
        if checkcode_input != checkcode_correct:
            template_var['status'] = 'fail'
            return HttpResponse(simplejson.dumps(template_var, ensure_ascii = False), content_type="application/json")
        
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
        
        try:
            corp = Corp.objects.get(name = corpName)
        except ObjectDoesNotExist:
            corp = Corp()
            corp.name = corpName
            corp.save()

        typos.phrases = inWord
        typos.sentence = inCentence
        typos.correct_phrases = correctWord
        typos.url = link
        typos.publisher = publisher
        typos.typos_hash = typos_hash
        typos.status = status
        typos.belongto = corpName
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

def userStatics(request, userid):
    template_var = {}
    
    typos = Typos.objects.filter(publisher = userid)
    userObj = User.objects.get(id = userid)

    name = userObj.username

    template_var['name'] = name

    typos_ing = [typo for typo in typos if typo.status == '0']
    typos_fail = [typo for typo in typos if typo.status == '1']
    typos_pass = [typo for typo in typos if typo.status == '2']
    typos_modified = [typo for typo in typos if typo.status == '3']

    typos_ing_count = len(typos_ing)
    typos_fail_count = len(typos_fail)
    typos_pass_count = len(typos_pass)
    typos_modified_count = len(typos_modified)

    template_var['typos_ing_count'] = typos_ing_count
    template_var['typos_fail_count'] = typos_fail_count
    template_var['typos_pass_count'] = typos_pass_count
    template_var['typos_modified_count'] = typos_modified_count

    template_var['typos_ing'] = typos_ing
    template_var['typos_fail'] = typos_fail
    template_var['typos_pass'] = typos_pass
    template_var['typos_modified'] = typos_modified
    
    return render_to_response("user.html",template_var, context_instance=RequestContext(request))

def rank(request):
    from django.db import connection,transaction
    template_var = {}
    cursor = connection.cursor()
    # belongto section
    # belongtoRaw = 'select typos.*, corp.name from (select belongto_id as bid, count(1) as ct from typos_typos group by bid) as typos join typos_corp as corp on typos.bid = corp.id order by ct desc'
    belongtoRaw = 'select belongto name, count(1) as ct from typos_typos group by name desc'
    cursor.execute(belongtoRaw)
    btrs = cursor.fetchall()
    btrsList = []
    
    for btr in btrs:
        td = {}
        td['name'] = btr[0]
        td['ct'] = btr[1]

        btrsList.append(td)

    template_var['btrs'] = btrsList
    # company section
    publisherRaw = 'select typos.*, au.username from (select publisher_id as pid, count(1) as ct from typos_typos group by pid) as typos join auth_user as au on typos.pid = au.id order by ct desc'
    cursor.execute(publisherRaw)
    ps = cursor.fetchall()
    psList = []
    
    for p in ps:
        td = {}
        td['pid'] = p[0]
        td['ct'] = p[1]
        td['name'] = p[2]

        psList.append(td)

    template_var['ps'] = psList

    return render_to_response("rank.html", template_var, context_instance=RequestContext(request))


def notice(request):
    template_var = {}

    return render_to_response("notice.html", template_var, context_instance=RequestContext(request))

def getcci(request):
    from PIL import Image, ImageDraw
    import random, cStringIO, os
    image = os.getcwd()+"/typos/static/images/black.png"
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    mp = hashlib.md5()
    mp_src = mp.update(str(datetime.datetime.now()))
    mp_src = mp.hexdigest()
    rand_str = mp_src[0:4]

    draw.text((10,10), rand_str[0])
    draw.text((48,10), rand_str[1])
    draw.text((85,10), rand_str[2])
    draw.text((120,10), rand_str[3])
    del draw
    request.session['checkcode'] = rand_str

    buf = cStringIO.StringIO()
    im.save(buf, 'png')
    return HttpResponse(buf.getvalue(),'image/png')

# for other app or web.
# 1. earthquake

def getEarth(request):
    template_var = []
    link = "http://www.csndmc.ac.cn/newweb/qq_events/index.html"
    linkPointer = urllib2.urlopen(link)

    contents = linkPointer.read()
    soup = BeautifulSoup(contents)

    tables = soup.find_all('table')
    infoTable = tables[3]
    trs = infoTable.findAll('tr')

    for i in range(1, len(trs)):
        tds = trs[i].findAll('td')
        quake = []
        for j in range(1, len(tds)):
            quake.append(tds[j].string)
        template_var.append(quake)
    
    return HttpResponse(simplejson.dumps(template_var, ensure_ascii = False), content_type="application/json")

    