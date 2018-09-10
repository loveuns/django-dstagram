# 미리 만들어져있는 시그널을 임포트
from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount

# 시그널이 발생했을 때 실행될 함수
def naver_signup(request, user, **kwargs):
    social_user = SocialAccount.objects.get(user=user)
    user.last_name = social_user.extra_data['name']
    user.save()

# 시그널과 해당 함수를 connect
user_signed_up.connect(naver_signup)
