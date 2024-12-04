from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .models import Post 
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
# from django.contrib.auth.decorators import login_required



# Create your views here.

def home_page(request):
    try:
        if not request.user.is_authenticated:
            raise Http404('User Not Authenticated')
        posts = Post.objects.all()
        return render(request,'home.html',{'posts':posts})
    except Http404:
        messages.error(request,'You Must Login First')
        return redirect('login_view')


def post_detail(request,id):
    if not request.user.is_authenticated:
        messages.error(request,'You Must Login First')
        return redirect('login_view')
    try:
        post = get_object_or_404(Post,id=id)
        return render(request,'post_detail_page.html',{'post': post})
    except Exception as e:
        messages.error(request,f'Error Occured:{str(e)}')
        return redirect('home_page')


def create_post(request):
    try:
        if not request.user.is_authenticated:
            messages.error(request,'You must log in to create a post.')
            return redirect('login_view')
      
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
        
            if not title or not content:
                messages.error(request,'Title and Content Cannot be Empty')
                return render(request,'create_post_page.html',)
            try:
                post = Post.objects.create(title= title,content=content)
                messages.success(request,'Post Successfully Created')
                return redirect('post_detail',id=post.id)
            except Exception as e:
                messages.error(request,f'Error Creating a Post:{str(e)}')
           
        return render(request,'create_post_page.html')

    except Exception as e:
        messages.error(request,f'Error Occured:{str(e)}')
        return redirect("home_page")



def edit_post(request,id):
    try:
        if not request.user.is_authenticated:
            messages.error(request,'You Must Login To Edit Post')
            return redirect('login_view')
        try:
           post = get_object_or_404(Post,id=id)
        except Post.DoesNotExist:
            messages.error(request,'Post Does Not Exist')
            return redirect('home_page')
    
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
        
            if not title or content:
                messages.error(request,'Title and Content Cannot be Empty')
                return render(request,'edit_post_page.html',{'post':post})
            try:
                post.title = title
                post.content = content
                post.save()
                messages.success(request,'Post Updated Successfully')
                return redirect('post_detail',id=post.id,)
            except Exception as e:
                messages.error(request,f'Error Updating Post{str(e)}')
                return render(request,'edit_post_page.html')
            
        return render(request,'edit_post_page.html',{'post':post})
    
    except Exception as e:
        messages.error(request,f'Error occured:{str(e)}')
        return redirect("home_page")




def delete_post(request, id):
    try:
        if not request.user.is_authenticated:
            messages.error(request,'You Must Log in')
            return redirect('login_view')
        
        post = get_object_or_404(Post, id=id)
        
        if request.method == "POST":
            try:
                post.delete()
                messages.success(request,'Post Succesfully Deleted')
                return redirect('home_page')
            
            except Exception as e:
                messages.error(request,f'Error Deleting the Post:{str(e)}')
                return redirect('home_page')
            
        return render(request,'delete_post_page.html', {'post': post})
    
    except Exception as e:
        messages.error(request,f'Error Occured:{str(e)}')
        return redirect('home_page')

    
    
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

def custom_404_view(request, exception):
    return render(request,'404.html',status=404)

def custom_500_view(request,exception):
    return render(request,'500.html',status=500)