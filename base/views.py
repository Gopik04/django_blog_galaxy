from django.shortcuts import render,redirect
from . models import *
from django.db.models import Q
from accounts.models import UserProfile
from.forms import PostForm
# Create your views here.
#home page
def post_category(request,category):
    posts=Post.objects.filter(category=category)
    recent_posts = Post.objects.all()[0:5]
    existing_category = Category.objects.all()
    return render(request,"index.html", {
            'posts':posts,
            'recent_posts':recent_posts,
            'existing_category':existing_category
            })
def home(request):
    if request.user.is_authenticated:
        filter_qury = request.GET.get('q') if request.GET.get('q') != None else ''
        #Search Engine
        posts = Post.objects.filter(
            Q(title__icontains = filter_qury) |
            Q(author__username__icontains=filter_qury) |
            Q(category__icontains=filter_qury)
            
        )
        profile=UserProfile.objects.get(person=request.user)
        recent_posts = Post.objects.all()[0:5]
        existing_category = Category.objects.all()
        return render(request,"index.html", {
            'posts':posts,
            'profile':profile,
            'recent_posts':recent_posts,
            'existing_category':existing_category
            })
    else:
        filter_qury = request.GET.get('q') if request.GET.get('q') != None else ''
        #Search Engine
        posts = Post.objects.filter(
            Q(title__icontains = filter_qury) |
            Q(author__username__icontains=filter_qury) |
            Q(category__icontains=filter_qury))
        recent_posts = Post.objects.all()[0:5]
        existing_category = Category.objects.all()
        return render(request,"index.html", {
            'posts':posts,
            'recent_posts':recent_posts,
            'existing_category':existing_category                                
            })
    
def read_post(request,id,slug):
    post=Post.objects.get(id=id,slug=slug)
    similar_post=Post.objects.filter(category=post.category)
    profile=UserProfile.objects.get(person=request.user)
    return render(request,'post.html',{'post':post,'profile':profile , 'similar_post':similar_post})

def update_post(request,id):
    post = Post.objects.get(id=id)
    if request.method=='POST':
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile',username=post.author.username, id=post.author.id)
    else:
        form = PostForm(instance=post)
        return render(request, 'update_post.html' , {'post':post, 'form':form})
    
def delete_post(request,id):
    post=Post.objects.get(id=id)
    if request.method=='POST':
        post.delete()
        return redirect('profile',username=post.author.username, id=post.author.id)
    else:
        return render(request, 'delete.html' , {'item':post,'type':'post'})
    