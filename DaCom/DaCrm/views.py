from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Client, Worker, Assignment
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm, ClientRegistrationForm, WorkerRegistrationForm
 


def home(request):
    return render(request, 'home.html')


@login_required
def client_dashboard(request):
    if request.user == 'is_client':
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
    if request.user == 'is_worker':
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


# Client registration view
def client_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        client_form = ClientRegistrationForm(request.POST)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save(commit=False)
            user.is_client = True
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            client = client_form.save(commit=False)
            client.user = user
            client.save()

            login(request, user)
            return redirect('client_dashboard')
    else:
        user_form = UserRegistrationForm()
        client_form = ClientRegistrationForm()
    return render(request, 'client_register.html', {'user_form': user_form, 'client_form': client_form})

# Worker registration view
def worker_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        worker_form = WorkerRegistrationForm(request.POST)
        if user_form.is_valid() and worker_form.is_valid():
            user = user_form.save(commit=False)
            user.is_worker = True
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            worker = worker_form.save(commit=False)
            worker.user = user
            worker.save()

            login(request, user)
            return redirect('worker_dashboard')
    else:
        user_form = UserRegistrationForm()
        worker_form = WorkerRegistrationForm()
    return render(request, 'worker_register.html', {'user_form': user_form, 'worker_form': worker_form})





def not_authorized_view(request):
    return render(request, 'not_authorized.html')

          
 
def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if hasattr(user, 'is_client'):
                    return redirect('client_dashboard')
                elif hasattr(user, 'is_worker'):
                    return redirect('worker_dashboard')
                else:
                    # Handle case where user is authenticated but neither client nor worker
                    return redirect('login')  # Redirect to a default page or error page
            else:
                # Handle case where authentication fails
                form.add_error(None, 'Invalid email or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')




