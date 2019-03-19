from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
import sweetify

from app.models import Estudante, Mentor
from app.auth import estudante_auth, mentor_auth
from app import forms

def cadastro(request):
	if request.POST.get('do', '') == 'cadastro_estudante':
		form_estudante = forms.EstudanteCadastroForm(request.POST)

		if form_estudante.is_valid():
			form_estudante.instance.senha = make_password(form_estudante.cleaned_data['senha'])
			estudante = form_estudante.save()
			estudante_auth.init_session(request, estudante)		

			sweetify.success(request, 'Cadastro concluído!', html='<p>Seu cadastro foi concluído!</p><p>Agora basta procurar e encontrar um mentor ideal para você.</p><p>Caso deseje entrar em contato com algum, basta clicar no botão e iremos solicitar o contato!', persistent=True)

			return redirect('app_estudante_home')	
	else:
		form_estudante = forms.EstudanteCadastroForm()

	if request.POST.get('do', '') == 'cadastro_mentor':
		form_mentor = forms.MentorCadastroForm(request.POST)

		if form_mentor.is_valid():
			form_mentor.instance.senha = make_password(form_mentor.cleaned_data['senha'])
			form_mentor.instance.curso = ""
			form_mentor.instance.instituicao = ""
			mentor = form_mentor.save()
			mentor_auth.init_session(request, mentor)		

			sweetify.success(request, 'Cadastro concluído!', html='<p>Seu cadastro foi concluído!</p><p>Agora basta aguardar que nossa equipe irá entrar em contato para analisar e aprovar seu cadastro!</p>', persistent=True)

			return redirect('app_auth_login')	
	else:
		form_mentor = forms.MentorCadastroForm()

	contexto = {
		'form_estudante': form_estudante,
		'form_mentor': form_mentor
	}

	return render(request, 'auth_cadastro.html', contexto)

def login(request):
	if request.POST.get("do", '') == "login_estudante":
		if estudante_auth.get(request) is None:
			form_estudante = forms.EstudanteLoginForm(request.POST)

			if form_estudante.is_valid():
				email = form_estudante.cleaned_data["email"]
				senha = form_estudante.cleaned_data["senha"]

				if estudante_auth.login(request, email, senha):
					return redirect("app_estudante_home")
				else:
					form_estudante.add_error("email", "E-mail e/ou senha inválidos.")
		else:
			return redirect('app_estudante_home')
	else:
		form_estudante = forms.EstudanteLoginForm()
					
	if request.POST.get('do', '') == 'login_mentor':
		if mentor_auth.get(request) is None:
			form_mentor = forms.MentorLoginForm(request.POST)

			if form_mentor.is_valid():
				email = form_mentor.cleaned_data['email']
				senha = form_mentor.cleaned_data['senha']

				if mentor_auth.login(request, email, senha):
					return redirect('app_mentor_home')
				else:
					form_mentor.add_error('email', 'E-mail e/ou senha inválidos.')
		else:
			return redirect('app_mentor_home')
	else:
		form_mentor = forms.MentorLoginForm()

	contexto = {
		'form_estudante': form_estudante,
		'form_mentor': form_mentor
	}

	return render(request, 'auth_login.html', contexto)

def logout(request):
	estudante_auth.logout(request)
	mentor_auth.logout(request)

	return redirect('app_auth_login')