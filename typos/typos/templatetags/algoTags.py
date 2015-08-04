#-*- coding: utf-8 -*-
'''
Created on 2014-7-26

@author: ekse
'''
from django import template

register = template.Library()

@register.filter()
def mod(value, arg):
    '''for mod operation, return remainder
    '''
    return value % arg

@register.filter()
def divide(value, arg):
    '''for divide operation, return n
    '''
    return value/arg
