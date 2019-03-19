from django.contrib.auth.hashers import make_password, check_password
from app.models import Mentor

def logout(request):
    if request.session.get('mentor_id') is not None:
        del request.session['mentor_id']

def init_session(request, mentor):
    request.session['mentor_id'] = mentor.id

def get(request):
    if request.session.get('mentor_id') is not None:
        id = request.session.get('mentor_id')
        if isinstance(id, int):
            try:
                return Mentor.objects.get(pk=int(id))
            except Mentor.DoesNotExist:
                pass

    return None

def login(request, email, senha):
    try:
        mentor = Mentor.objects.get(email=email)

        if(check_password(senha, mentor.senha)):
            init_session(request, mentor)
            return mentor
    except Mentor.DoesNotExist:
        pass

    return None