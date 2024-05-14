from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(user_logged_out, sender=User)
def user_logged_out_handler(sender, request, user, **kwargs):
    # 根据用户的权限来决定登出后跳转的网页
    if user.is_staff('app.change_model'):
        logout_url = '/accounts/login/'
    else:
        logout_url = '/user/logout/'

    # 设置登出后跳转的网页
    request.session['_logout_url'] = logout_url