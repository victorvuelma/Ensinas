from django.contrib.auth.hashers import make_password, check_password
from app.models import Estudante

def logout(request):
    del request.session["estudante_id"]
    request.session.modified = True

def get(request):
    if request.session.get("estudante_id") is not None:
        id = request.session.get("estudante_id")
        if isinstance(id, int):
            id = int(id)
            try:
                estudante = Estudante.objects.get(pk=id)
                return estudante
            except Estudante.DoesNotExist:
                pass

    return None
    
def login(request, email, senha):
    try:
        estudante = Estudante.objects.get(email=email)

        if(check_password(senha, estudante.senha)):
            request.session["estudante_id"] = estudante.id
            request.session.modified = True
            return True
    except Estudante.DoesNotExist:
            pass

    return False