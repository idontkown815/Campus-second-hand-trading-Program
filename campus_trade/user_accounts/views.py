from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.
def register(request):
    """用户注册视图"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # 使用学号作为用户名
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('student_id')
            user.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f'注册成功！欢迎 {name}')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'user_accounts/register.html', {'form': form})
