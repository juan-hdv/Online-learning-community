from django import template

register = template.Library()

@register.filter(name='filter_by_user')
def filter_by_user(modelList, user):
    return modelList.filter(user=user).first()
