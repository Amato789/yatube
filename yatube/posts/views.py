from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  "index.html",
                  {"page": page, "paginator": paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date").all()
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  "group.html",
                  {"group": group, "page": page, "paginator": paginator})


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('index')
    return render(request, 'new_post.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('author',)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {"paginator": paginator, "author": author, "page": page})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_detail.html', {"post": post})


def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('post_detail', post_id=post.pk)
    form = PostForm(request.POST or None, instance=post)
    is_edit = True
    if form.is_valid():
        form = form.save(commit=False)
        form.save()
        return redirect('post_detail', post_id=post.pk)
    return render(request, 'new_post.html', {'form': form, 'is_edit': is_edit, 'post': post})
