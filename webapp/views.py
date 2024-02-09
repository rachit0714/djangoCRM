from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

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
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.clean_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have Successfully Registered! You are now logged in!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def get_clients(request):
    records = Record.objects.all()
    return render(request, 'clients.html', {'records': records})

def client_record(request, pk):
    if request.user.is_authenticated:
        client_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'client': client_record})
    else:
        messages.success(request, "You must be logged in to view that page.")
        return redirect('home')
    
def delete_client(request, pk):
    if request.user.is_authenticated:
        if request.user.is_staff:
            rec_to_del = Record.objects.get(id=pk)
            rec_to_del.delete()
            messages.success(request, "Record has been successfully deleted")
        else:
            messages.success(request, "You must be a staff to delete a user")
    else:
        messages.success(request, "You must be staff logged in delete a client")
    return redirect('clients')

def add_client(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect("clients")
        return render(request, 'add_client.html', {'form': form})
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')
    
def update_client(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, f"Record {pk} has been updated")
            return redirect('clients')
        return render(request, 'update_client.html', {'form': form, 'pk':pk})
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')


