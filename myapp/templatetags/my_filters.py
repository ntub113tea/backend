from django import template

register = template.Library()

@register.filter
def mask_phone(phone):
    if phone and len(phone) > 3:
        return phone[:-3] + 'xxx'
    return phone