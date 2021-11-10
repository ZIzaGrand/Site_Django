from django import template
from souvenir.models import *

register = template.Library()


@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)

@register.inclusion_tag('souvenir/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('souvenir/list_souvenirs.html')
def show_souvenirs(cat_selected):
    if not cat_selected:
        posts = Souvenir.objects.filter(availability=True).select_related('cat')
    else:
        posts = Souvenir.objects.filter(cat_id__slug=cat_selected)
        print(posts)

    return {'posts': posts}