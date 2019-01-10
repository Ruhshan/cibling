from django.shortcuts import render
from .models import Post,Comment
from django.contrib.auth.models import User
from users.models import Profile
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse

# Create your views here.

author_imgs={
    'Diana': 'images/users/user-11.jpg',
    'Sarah': 'images/users/user-1.jpg',
    'John': 'images/users/user-4.jpg',
}

comments=[
    {
        'author': 'Diana',
        'content': 'iet dolore magna aliqua. Ut enim ad minim veniam, quis nostrud',
        'authorimg': author_imgs['Diana']
    },
    {
        'author': 'John',
        'content': 'd ut labore et dolore magna aliqua. Ut enim ad minim veniam, q',
        'authorimg': author_imgs['John']
    },
    {
        'author': 'Diana',
        'content': 'sit amet, consncididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud',
        'authorimg': author_imgs['Diana']
    },
    {
        'author': 'John',
        'content': 'ampor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, q',
        'authorimg': author_imgs['John']
    },
]

posts=[
    {
        'author': 'Sarah',
        'time': 'about 15 mins ago',
        'imageurl': 'images/post-images/12.jpg',
        'userimgurl': 'images/users/user-1.jpg',
        'likes': 13,
        'dislikes': 0,
        'content': 'Lo occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'comments': comments[0:2]
    },
    {
        'author': 'Sarah',
        'time': 'yesterday',
        'imageurl': 'images/post-images/13.jpg',
        'userimgurl': 'images/users/user-1.jpg',
        'likes': 13,
        'dislikes': 0,
        'content': 'adipiscing elit, Lo occaecat cupidatat  culpa qui officia deserunt mollit anim id est laborum.',
        'comments': comments[2:4]

    },

]



def Timeline(request):
    context={
        #'posts': Post.objects.all(),
        'posts': posts,
        'author_imgs': author_imgs
    }

    return render(request, 'cibling_web/timeline.html', context)

def Newsfeed(request):
    posts=Post.objects.all()
    comments=Comment.objects.all()

    context={
        'posts':posts,
        'comments':comments,
        'user': request.user
    }

    return render(request, 'cibling_web/newsfeed.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'cibling_web/timeline.html'
    context_object_name = 'posts'
    ordering = ['-time_posted']

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



def timeline_profile(request, pk):
    posts = Post.objects.all()
    comments = Comment.objects.all()

    context = {
        'posts':posts,
        'comments':comments,
        'user': User.objects.filter(id=pk).first()
    }
    return render(request, 'cibling_web/timeline_profile.html', context)

def timeline_profile_about(request,pk):
    posts = Post.objects.all()
    comments = Comment.objects.all()

    context = {
        'posts': posts,
        'comments': comments,
        'user': User.objects.filter(id=pk).first()
    }
    return render(request, 'cibling_web/timeline_profile_about.html', context)