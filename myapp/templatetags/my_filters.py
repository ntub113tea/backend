from django import template

register = template.Library()

@register.filter
def mask_phone(phone):
    if phone and len(phone) > 3:
        return 'xxxx-'+phone[4:7] +'-'+phone[7:10] 
    return phone