from django.conf import settings
from django.core.mail import send_mail

from match.models import Match


def check_macthing(match):
    """
    Проверяет наличия взаимной симпатии
    в случае совпадения отправляет рассылку
    """
    user = match.user
    match = match.matching
    if not Match.objects.filter(user=match, matching=user, mark=True).exists():
        return

    return send_match(user, match), send_match(match, user)


def send_match(user, matching):
    """
    Рассылает участникам информацию о совпадении
    """
    subject = 'У вас есть пара!'
    message = f'Вы понравились {matching.first_name}!  Почта участника: {matching.email}'
    admin_email = settings.ADMIN_EMAIL
    user_email = [user.email]
    return send_mail(subject, message, admin_email, user_email)


def get_client_ip(request):
    """
    Возвращает айпи, с которого пришел запрос
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
