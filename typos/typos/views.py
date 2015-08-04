#-*- coding: utf-8 -*-
'''
Created on 2015-08-04

@author: ekse
'''
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render_to_response
from django.template import RequestContext
from product.models import *
from article.models import *

def home(request):
    template_var = {}
    # products
    #product_list = Product.objects.all()[:4]
    # news
    #news_list = Article.objects.order_by('publish_date')[:10]
    
    #template_var['news_list'] = news_list
    #template_var['product_list'] = product_list
    
    return render_to_response("index.html",template_var, context_instance=RequestContext(request))


def contact(request):
    template_var = {}
    return render_to_response("contacts.html",template_var, context_instance=RequestContext(request))

