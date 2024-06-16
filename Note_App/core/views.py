from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from core.forms import NoteForm
from core.models import Note

@login_required(login_url='login_page')
def home(request):
    notes = Note.objects.filter(user=request.user) 
    return render(request, 'core/home.html', {'notes': notes})


def logout_page(request):
    logout(request)
    return redirect('login_page')

def about(request):
    return render(request, 'core/about.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('login_page')
        
        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('login_page')
        else:
            login(request, user)
            return redirect('Home')

    return render(request, 'core/login.html')

def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'User Already Exists')
            return redirect('register_page')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password
        )
        
        messages.success(request, 'Account Created Successfully')
        return redirect('login_page')

    return render(request, 'core/register.html')



@login_required(login_url='login_page')
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'backend/note_detail.html', {'note': note})

@login_required(login_url='login_page')
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, 'New note added successfully!')
            return redirect('Home')
    else:
        form = NoteForm()
    return render(request, 'backend/note_form.html', {'form': form})

@login_required(login_url='login_page')
def note_edit(request, pk=None):
    if pk:
        note = get_object_or_404(Note, pk=pk)
    else:
        note = None

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save()
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)

    return render(request, 'backend/note_form.html', {'form': form, 'note': note})


@login_required(login_url='login_page')
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('Home')
    return render(request, 'backend/note_confirm_delete.html', {'note': note})
