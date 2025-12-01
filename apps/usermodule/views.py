from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages  # لاستخدام الرسائل (Task 5) [cite: 67]

# ----------------------------------------
# Lab 12 - Task 1: Register User [cite: 63]
# ----------------------------------------
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Task 5: رسالة نجاح التسجيل [cite: 67]
            messages.success(request, 'You have successfully registered')
            return redirect('login_user')
        else:
            # Task 5: رسالة خطأ [cite: 67]
            messages.error(request, 'Error message: Registration failed')
    else:
        form = UserCreationForm()
    
    return render(request, 'usermodule/register.html', {'form': form})

# ----------------------------------------
# Task 2: Login User [cite: 64]
# ----------------------------------------
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Task 5: رسالة نجاح الدخول [cite: 67]
            messages.success(request, 'Login successfully')
            return redirect('list_students') # توجيه لصفحة من اللاب السابق
        else:
            # Task 5: رسالة خطأ [cite: 67]
            messages.error(request, 'Error message: Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'usermodule/login.html', {'form': form})

# ----------------------------------------
# Task 4: Logout User 
# ----------------------------------------
def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login_user')