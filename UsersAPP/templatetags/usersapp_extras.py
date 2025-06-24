import json
 
from django import template
 
register = template.Library()
 
@register.filter
def canSeeProduct(user, code):
    return user.canSeeProduct(code=code)

@register.filter
def canSeeAPP(user, code):
    return user.canSeeAPP(code=code)

@register.filter
def get_at_index(list, index):
    return list[index]