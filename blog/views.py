from django.shortcuts import render


# Create your views here.
from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import redirect, render, get_object_or_404
from .forms import PostForm


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'posts': Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    })


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {
        'form': form, 
        'posts': Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    })


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.image = form.cleaned_data['image']

            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {
        'form': form,
        'posts': Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    })
