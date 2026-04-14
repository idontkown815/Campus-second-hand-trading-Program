from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.
def register(request):
    """用户注册视图"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'注册成功！欢迎 {username}')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'user_accounts/register.html', {'form': form})
