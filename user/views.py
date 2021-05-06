from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm,EditProfileForm
from .models import User
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


#################### index#######################################
def index(request):
	return render(request, 'index.html', {'title':'index'})

########### register here #####################################
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			# username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			######################### mail system ####################################
			htmly = get_template('Email.html')
			d = { 'email': email }
			subject, from_email, to = 'welcome', 'bookmyseva.services@gmail.com', email
			html_content = htmly.render(d)
			msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			##################################################################
			messages.success(request, f'Your account has been created ! You are now logged in')
			new_user=authenticate(email=form.cleaned_data['email'],password=form.cleaned_data['password1'],)
			login(request, new_user)
			return redirect('/')
	else:
		form = UserRegisterForm()
	return render(request, 'register.html', {'form': form, 'title':'register here'})

################ login forms###################################################
def Login(request):
	if request.method == 'POST':

		# AuthenticationForm_can_also_be_used__

		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(request, email = email, password = password)
		if user is not None:
			form = login(request, user)
			messages.success(request, f' welcome {email} !!')
			return redirect('index')
		else:
			messages.info(request, f'account done not exit plz sign in')
	form = AuthenticationForm()
	return render(request, 'login.html', {'form':form, 'title':'log in'})

def profile_info(request):
	if request.method == 'POST':
		current_user=request.user
		current_user.delete()
		return redirect('/')
	return render(request, 'profile.html', {'title':'profile'})

def prof_list(request):
	profs = User.objects.all().exclude(is_admin=True)
	servs = User.objects.values('main_service').distinct().exclude(is_admin=True)
	return render(request,'services.html',{'profs':profs,'servs':servs})

def edit_profile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('/')
	else:
		form = EditProfileForm(instance=request.user)
		return render(request, 'edit_profile.html', {'form':form})
