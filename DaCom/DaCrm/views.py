from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import CustomUser, Client, Worker, Assignment
from django.contrib.auth.decorators import login_required


@login_required
def client_dashboard(request):
    user = request.user
    if user.user_type != 'client':
        return redirect('home')  # Or some other page

    client = get_object_or_404(Client, user=user)
    assignments = Assignment.objects.filter(client=client)
    
    context = {
        'client': client,
        'assignments': assignments,
    }
    return render(request, 'client_dashboard.html', context)


@login_required
def worker_dashboard(request):
    if hasattr(request.user, 'worker'):
        worker = request.user.worker
        assignments = Assignment.objects.filter(worker=worker)
        context = {
            'worker': worker,
            'assignments': assignments
        }
        return render(request, 'worker_dashboard.html', context)
    else:
        return render(request, 'not_authorized.html')


def home(request):
    return render(request, 'home.html')


def register_page(request):
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.save()

            if user.user_type == 'client':
                Client.objects.create(
                    user=user,
                    company_name=form.cleaned_data.get('company_name'),
                    state=form.cleaned_data.get('state'),
                    lga=form.cleaned_data.get('lga'),
                )
            elif user.user_type == 'worker':
                Worker.objects.create(
                    user=user,
                    first_name=form.cleaned_data.get('first_name'),
                    last_name=form.cleaned_data.get('last_name'),
                    state=form.cleaned_data.get('state'),
                    lga=form.cleaned_data.get('lga'),
                    phone_number=form.cleaned_data.get('phone_number'),
                )

            login(request, user)
            return redirect('client_dashboard')  # Redirect to a homepage or another page after signup
        else:
            form = CustomUserCreationForm()
        
        return render(request, 'register.html', {'form': form})

          
 
def login_page(request):
    
    #check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Authenticate

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "you have been logged in ")
            return redirect('client_das')
        else:
            messages.success(request, "Thers was an Error Logging in please try again...")
            return redirect('home')
    else:
        return render(request, 'home.html')
    