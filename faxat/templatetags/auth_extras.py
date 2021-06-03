from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name = 'has_group')
def has_group(user, group_name):
    try :
        group = Group.objects.get(name = group_name)
    except :
        return False

    return True if group in user.groups.all() else False
# 
# @register.filter(name = 'get_dept')
# def get_dept(user, group_name):
#     try :
#         group = Group.objects.get(name = group_name)
#     except :
#         return False
#
#     return True if group in user.groups.all() else False
