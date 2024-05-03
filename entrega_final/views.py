from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, BlogForm
from .models import Blog
import logging

def index(request):
    blogs = Blog.objects.all()
    return render(request, 'index.html', {'blogs': blogs})

def about(request):
    return render(request, 'about.html')

@login_required
def post_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            image = form.cleaned_data['image']
            author = request.user
            blog = Blog(title=title, content=content, image=image, author=author)
            blog.save()
            return redirect('blog')
    else:
        form = BlogForm()
    return render(request, 'blog.html', {'form': form})

def careers(request):
    return render(request, 'careers.html')

def contact(request):
    return render(request, 'contact.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:               
                return render(request, 'login.html', {'form': form, 'error_message': 'Nombre de usuario o contraseña incorrectos'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def blog(request):
    blogs = Blog.objects.all()
    return render(request, 'blog.html', {'blogs': blogs})

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    blogs = Blog.objects.filter(author=user)
    blog_form = BlogForm()
    return render(request, 'profile.html', {'user': user, 'blogs': blogs, 'blog_form': blog_form})

@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'edit_blog.html', {'form': form, 'blog': blog})

logger = logging.getLogger(__name__)

@require_POST
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.user == blog.author:
        blog.delete()
        logger.info(f"La entrada del blog con ID {blog_id} ha sido eliminada.")
    else:
        logger.warning("Intento de eliminación de entrada de blog por un usuario no autorizado.")
   
    return redirect('blog')