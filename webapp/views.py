from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def home(request):
    # Checks to see if the user is logging in
    if request.method == "POST":
        validate = login_user(request)
        if validate == True:
            return redirect("home")
        else:            
            return redirect("home")        
    return render(request, 'home.html', {})

def login_user(request):
    user_name = request.POST["username"]
    password = request.POST["password"]
    # Authenticate
    user = authenticate(request, username=user_name, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, "Login sucessful")
        return True
    else:
        messages.success(request, "Invalid username or password")
        return False



def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')

def register_user(request):
    return render(request, 'register.html', {})
