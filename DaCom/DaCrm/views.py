from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from .models import Client, Worker, Assignment, CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
 


def home(request):
    return render(request, 'home.html')


@login_required
def client_dashboard(request):
    if request.user.user_type == 'client':
        # Retrieve the Client instance related to the current user
        client = get_object_or_404(Client, user=request.user)
        assignments = Assignment.objects.filter(client=client)
        context = {
            'client': client,
            'assignments': assignments
        }
        return render(request, 'client_dashboard.html', context)
    else:
        return render(request, 'not_authorized.html')


@login_required
def worker_dashboard(request):
    if request.user.user_type == 'worker':
        # Retrieve the Client instance related to the current user
        worker = get_object_or_404(Worker, user=request.user)
        assignments = Assignment.objects.filter(worker=worker)
        context = {
            'worker': worker,
            'assignments': assignments
        }
        return render(request, 'worker_dashboard.html', context)
    else:
        return render(request, 'not_authorized.html')



def register_page(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.save()

                user_type = user.user_type
                profile_data = {
                    'user': user,
                    'state': form.cleaned_data.get('state'),
                    'lga': form.cleaned_data.get('lga'),
                    'phone_number': form.cleaned_data.get('phone_number'),
                }

                if user_type == 'client':
                    profile_data['company_name'] = form.cleaned_data.get('company_name')
                    Client.objects.create(**profile_data)
                    login(request, user)
                    return redirect('client_dashboard')
                elif user_type == 'worker':
                    Worker.objects.create(**profile_data)
                    login(request, user)
                    return redirect('worker_dashboard')
            except IntegrityError:
                form.add_error('username', 'Username already exists. Please choose another one.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})



def not_authorized_view(request):
    return render(request, 'not_authorized.html')

          
 
def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if hasattr(user, 'client'):
                    return redirect('client_dashboard')
                elif hasattr(user, 'worker'):
                    return redirect('worker_dashboard')
                else:
                    # Handle case where user is authenticated but neither client nor worker
                    return redirect('login')  # Redirect to a default page or error page
            else:
                # Handle case where authentication fails
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')




