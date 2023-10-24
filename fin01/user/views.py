

from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import User
from django.contrib import messages

def register(request):
    if request.user.is_authenticated: 
        return redirect('/dashboard/') 
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/user/login/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})



from django.contrib.auth.views import LoginView
from django.urls import path, reverse_lazy

class MyLoginView(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')
    def get_success_url(self):
        return self.success_url

def login(request): 
    if request.user.is_authenticated: 
        return redirect('/dashboard/') 
    else: 
        return MyLoginView.as_view()(request)

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('/user/login/')


def get_user_info(request):
  user = get_user_model().objects.get(id=request.user.id)
  form = CustomPasswordChangeForm(user=request.user)
  return render(request, 'home/user.html' , context={'user' : user.username , 'user_info' : user , 'form' : form})

from .forms import CustomPasswordChangeForm
def reset_password(request):
    user = get_user_model().objects.get(id=request.user.id)
    form = CustomPasswordChangeForm(user=request.user)
    message = 'Đổi mật khẩu  không thành công'
    
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            message = 'Đổi mật khẩu thành công'
            logout(request)
            return redirect('/user/login/')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'home/user.html' , context={'user' : user.username , 'user_info' : user , 'form' : form , 'message' : message})

def deposit(request):
    if request.method == 'POST':
        req_amount= request.POST['amount']
        try:
            amount = int(req_amount)
        except ValueError:
            messages.error(request, 'Invalid Amount')
            return redirect('dashboard' )
        
        user =request.user 
        user.balance += amount
        user.save()
        return redirect('dashboard')        
    return render(request , 'user/deposit.html' )