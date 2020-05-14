from django import template
from core.models import library, bookmark, comparison

register = template.Library()


@register.filter
def added_to_bookmark(user, id):
    try:
        if user.is_authenticated:
            qs = bookmark.objects.filter(user=user)[0]
            # if qs.exists():
            if qs.libraries.filter(id=id).exists():
                return True
    except:
        return False


@register.filter
def added_to_compare(library_ids, id):
    if library_ids:
        if id in library_ids:
            return True
        else:
            return False
    else:
        return False

