from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    '''
    The home screen and login screen, if user is not logged in yet
    Params: request that has been sent
    Return: The home webpage
    '''
    if request.method == "POST":
        validate = login_user(request)
        if validate == True:
            return redirect("home")
        else:            
            return redirect("home")        
    return render(request, 'home.html', {})


def login_user(request):
    '''
    The login process for a user
    Params: request that has been sent
    Return: Boolean that validates a successful login attempt
    '''
    user_name = request.POST["username"]
    password = request.POST["password"]
    # Authentication to see if the user is in the system
    user = authenticate(request, username=user_name, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, "Login sucessful")
        return True
    else:
        messages.success(request, "Invalid username or password")
        return False

# logouts the user
def logout_user(request):
    '''
    The logout process for a user
    Params: request that has been sent
    Return: The login screen from the home webpage
    '''
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')

# creates a new user
def register_user(request):
    '''
    The registeration process for a user
    Params: request that has been sent
    Return: The home page upon a successful registration, otherwise the registration page again with an indicator on what to do
    '''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login user
            username = form.cleaned_data['username']
            password = form.clean_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have Successfully Registered! You are now logged in!")
            return redirect('home')
    else:
        # resends the register page
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})

def get_clients(request):
    '''
    Gives the view for all of the clients
    Params: request that has been sent
    Return: The record of all clients from the Record Model
    '''
    records = Record.objects.all()
    return render(request, 'clients.html', {'records': records})

# Opens the page of a specific client
def client_record(request, pk: int):
    '''
    Gives the view for a record inputed
    Params: request that has been sent and the id of the client that the user is requesting
    Return: The record of the client requested
    '''
    if request.user.is_authenticated:
        # Checks if there is an client with the requested id
        try:
            client_record = Record.objects.get(id=pk)
            return render(request, 'record.html', {'client': client_record})
        except:
            messages.success(request, f"There is no client with id {pk}")
            return redirect('clients')
    else:
        messages.success(request, "You must be logged in to view that page.")
        return redirect('home')
    
def delete_client(request, pk: int):
    '''
    Deletes the requested client from the system
    Params: request that has been sent and the id of the client that needs to be deleted
    Return: The page that lists all of the clients
    '''
    if request.user.is_authenticated:
        if request.user.is_staff:
            # Receives the user from Record and then deletes it
            rec_to_del = Record.objects.get(id=pk)
            rec_to_del.delete()
            messages.success(request, "Record has been successfully deleted")
        else:
            messages.success(request, "You must be a staff to delete a user")
    else:
        messages.success(request, "You must be staff logged in delete a client")
    return redirect('clients')

def add_client(request):
    '''
    Adds a new client to the record
    Params: request that has been sent
    Return: The record of all clients from the Record Model upon a valid form entry
    '''
    # Creates a form that the user will fill out for creating a new client
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == "POST":
                # If form has been successfully compeleted the new client is added to the records
                if form.is_valid():
                    add_record = form.save()
                    messages.success(request, "Record Added...")
                    return redirect("clients")
            return render(request, 'add_client.html', {'form': form})
        else:
            messages.success(request, "You must be staff to add clients")
            return redirect("clients")
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')
    
def update_client(request, pk: int):
    '''
    Lets the user update any inaccurate client information
    Params: request that has been sent and the id of the client that needs to be updated
    Return: The record of all clients from the Record Model
    '''
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

def search(request):
    '''
    Allows across the webapp, searches in the name and address columns of the clients page
    Params: request that has been sent
    Return: A page that lists matching results
    '''
    if request.method == "POST":
        # Checks if information is contained in either the clients name column or address column
        # All results are shown
        input = request.POST['search_input']
        clients_results = Record.objects.filter(first_name__contains=input) | Record.objects.filter(last_name__contains=input)
        address_results = Record.objects.filter(address__contains=input) | Record.objects.filter(city__contains=input) | Record.objects.filter(province__contains=input)
        return render(request, 'search.html', {'search_input': input, 'clients': clients_results, 'addresses': address_results})
    else:
        return render(request, 'search.html', {})

