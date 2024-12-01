from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .models import Post 
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
def home_page(request):
    posts = Post.objects.all()
    return render(request,'home.html',{'posts':posts})

@login_required
def post_detail(request,id):
    post = get_object_or_404(Post,id=id)
    return render(request,'post_detail_page.html', {'post': post})

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(title= title,content=content)
        return redirect('post_detail',id=post.id)
    return render(request,'create_post_page.html')

@login_required
def edit_post(request,id):
    post = get_object_or_404(Post,id=id)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('post_detail',id=post.id,)
    return render(request,'edit_post_page.html',{'post':post})

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        post.delete()
        return redirect('home_page')
    return render(request, 'delete_post_page.html', {'post': post})
    
    
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("home_page")
        else:
            messages.error(request,'Invalid Username or Password')
    return render(request,'login.html')
        
        
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request,'password does not match')
        elif User.objects.filter(username=username).exists():
            messages.error(request,'username already exixts')
        else:
            User.objects.create_user(username=username,password=password)
            messages.success(request,'Account created Successfully')
            return redirect('login_view')
        
    return render(request,'register.html')        
            

def logout_view(request):
    logout(request)
    request.session.flush()  # Clear the session data
    response = redirect('login_view')
    response.delete_cookie('sessionid')
    response.delete_cookie('csrftoken')
    return response