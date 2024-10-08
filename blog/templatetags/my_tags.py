from django import template

register = template.Library()


@register.filter
def mediapath(path):
    return "/media/" + str(path)


@register.simple_tag
def mediapath(path):
    return "/media/" + str(path)
