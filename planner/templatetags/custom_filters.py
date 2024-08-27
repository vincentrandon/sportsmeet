from django import template

register = template.Library()

@register.filter
def initials(value):
    try:
        names = value.split()
        initials = ''.join([name[0].upper() for name in names if name])
        return initials
    except Exception as e:
        return ''

@register.filter
def get_item(lst, index):
    try:
        return lst[int(index)]
    except (IndexError, ValueError):
        return None