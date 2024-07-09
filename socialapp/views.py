from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from socialapp.models import User,Post,likepost
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# from socialapp.utils import find_no_of_likes_received_by_user


# Create your views here.

def base(request):
    page_name = "base.html"
    return render(request,page_name)


@csrf_exempt
def sign_up(request):
    page_name="sign_up.html"
    if request.method =="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        
        if User.objects.filter(username=username).exists():
            return render(request,page_name,{"error":True,"error_msg":"username already exists"})
        
        if User.objects.filter(email=email).exists():
            return render(request,page_name,{"error":True,"error_msg":"email already exists"})
        user=User.objects.create_user(username=username,email=email,password=password)
        user=auth.authenticate(username=username,email=email,password=password)
        if user:
            auth.login(request,user)
            return redirect({"profile_settings"})
        else:
            return render(request,page_name,{"error_msg":"some error found"})
    else:
        return render(request,page_name)
    
@csrf_exempt
def sign_in(request):
    page_name="sign_in.html"
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user=auth.authenticate(username=username,password=password)
        if user:
            auth.login(request,user)
            return redirect('profile_settings')
        else:
            return render(request,page_name,{"error_msg": "Invalid username or password"})
    else:
        return render(request,page_name)


            
@login_required(login_url='sign_in')
def sign_out(login_url="sign_in"):
        auth.logout(request)
        return redirect('sign_up')
    
@login_required(login_url='sign_in')    
def profile_settings(request):
    user=request.user
    page_name = "profile_settings.html"
    data={
             "no_of_posts_created": user.Post.count(),
             "no_of_likes_done": user.like_post.count(),
            #  "no_of_likes_received": find_no_of_likes_received_by_user(user)
    }
    return render(request,page_name,data)


def index(request):
    page_name='index.html'
    data={
        "Post_list":Post.objects.all().order_by('-created_at'),
        # "already_liked_post_ids_of_current_user":User.like_post.values_list('post_id',flat=True)
    }
    return render(request,page_name,data)

@login_required(login_url='sign_in')
def add_post(request):
    
    user = request.user
    captions = request.POST['captions']
    Post.objects.create(user=user, captions=captions)
    return redirect('index')

@login_required(login_url='sign_in') 
def like_post(request,post_id):
        user = request.user
        post = Post.objects.get(id=post_id)
        likepost.objects.create(post_id=post_id, user_id=user.id)
        return redirect('index')


    
        
       
