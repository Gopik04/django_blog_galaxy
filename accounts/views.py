from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .models import UserProfile
from base.models import Post
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request,'login.html',{'error':True})
    return render(request,'login.html')
        
        
def user_logout(request):
    logout(request)
    return redirect('home')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        firstname=request.POST.get('first-name')
        lastname=request.POST.get('last-name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        password2=request.POST.get('password2')
        email=request.POST.get('email')
        
        about=request.POST.get('about')
        talks_about=request.POST.get('talks_about')
        
        avatar = request.FILES.get('file-upload')
        
        if password==password2:
            user=User.objects.create_user(username=username,password=password)
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.save()
            
            profile = UserProfile(
                person = user,
                about = about,
                talks_about = talks_about,
                avatar = avatar
            )
            profile.save()
            
            login(request,user)
            return redirect('home')
        else:   
            return render(request,'signup.html',{'error':True})
        
    return render(request,'signup.html')


def user_profile(request,username,id):
    user= User.objects.get(username=username,id=id)
    profile = UserProfile.objects.get(person=user)
    posts = Post.objects.filter(author=user)
    return render(request,'profile.html',{
        'profile':profile , 
        'posts':posts
    })
    
@login_required(login_url='login')  
def update_profile(request,username,id):
    user = User.objects.get(username=username, id=id)
    profile = UserProfile.objects.get(person=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        
        if form.is_valid():
            form.save()
            return redirect('profile',username=user.username,id=user.id)
    else:
        form = UserProfileForm(instance=profile)
    return render(request,'update_profile.html',{'form':form,'profile':profile})