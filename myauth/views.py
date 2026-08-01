from django.contrib.auth.views import LogoutView
from django.http import HttpResponse



class MyLogoutView(LogoutView):
    next_page = 'login'


def cookies_read(request):
    value = request.COOKIES.get('my_cookie', 'Куки не найдены')
    return HttpResponse(f'Cookie: {value}')


def cookies_set(request):
    response = HttpResponse('Cookie установлена')
    response.set_cookie('my_cookie', 'hello_cookie')
    return response


def session_read(request):
    value = request.session.get('my_session', 'Сессия не найдена')
    return HttpResponse(f'Session: {value}')


def session_set(request):
    request.session['my_session'] = 'hello_session'
    return HttpResponse('Session установлена')