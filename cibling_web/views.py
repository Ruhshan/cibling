from django.shortcuts import render, redirect
from .models import Post,Comment
from django.contrib.auth.models import User
from django.contrib import messages
from users.models import Profile, ProfileInfo, Cibling
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from .models import Post
from django.db import models
from .forms import PostForm
from django.contrib.auth.decorators import login_required


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

@login_required
def Newsfeed(request):
    if request.method!='POST':
        form = PostForm()
        user = request.user
        '''
        ciblings_1 = Cibling.objects.filter(cibling_1=user, status=False)
        ciblings_2 = Cibling.objects.filter(cibling_2=user, status=False)
        user_ciblings = []

        for cibling in ciblings_1:
            user_ciblings.append(cibling.cibling_2)
        for cibling in ciblings_2:
            user_ciblings.append(cibling.cibling_1)

        user_ciblings.append(user)
        posts=[]
        for userc in user_ciblings:
            postc=Post.objects.filter(author=userc)
            for post in postc:
                posts.append(post)
        '''
        posts=Post.objects.all()
        comments=Comment.objects.all()

        context={
            'posts':posts,
            'comments':comments,
            'user': request.user,
            'form': form,
            'title': 'Newsfeed'
        }

        return render(request, 'cibling_web/newsfeed.html', context)
    else:
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('newsfeed')

@login_required
def timeline_profile(request, pk):
    if request.method!='POST':
        form = PostForm()
        posts=Post.objects.all()
        comments=Comment.objects.all()
        user=User.objects.filter(id=pk).first()

        context={
            'posts':posts,
            'comments':comments,
            'user': User.objects.filter(id=pk).first(),
            'form': form,
            'pk': pk,
            'title': '{fname} {lname} Profile'.format(fname=user.first_name, lname=user.last_name)
        }

        return render(request, 'cibling_web/timeline_profile.html', context)

    else:
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            #needs to be fixed
            return redirect('newsfeed')


@login_required
def timeline_profile_about(request,pk):
    user = User.objects.filter(id=pk).first()
    profileinfo = user.profile.profileinfo
    #posts = Post.objects.all()
    #comments = Comment.objects.all()
    ec = profileinfo.expertises.all().exists()
    ic = profileinfo.interests.all().exists()
    lc = profileinfo.languages.all().exists()
    expertises = profileinfo.expertises.all()
    interests = profileinfo.interests.all()
    languages = profileinfo.languages.all()

    context = {
        'user': user,
        'profileinfo': profileinfo,
        'ec': ec,
        'ic': ic,
        'lc': lc,
        'expertises': expertises,
        'interests': interests,
        'languages': languages,
        'pk': pk,
        'title': '{fname} {lname} Profile Info'.format(fname=user.first_name, lname=user.last_name)
    }
    return render(request, 'cibling_web/timeline_profile_about.html', context)

@login_required
def add_cibling(request, pk):
    user2 = User.objects.filter(id=pk).first()
    user1 = request.user
    c = Cibling.objects.create(cibling_1=user1, cibling_2=user2)
    c.save()

    messages.success(request, 'Cibling request sent to {}'.format(user2.first_name+' '+user2.last_name))
    return redirect('newsfeed')

@login_required
def accept_cibling(request, pk):
    user2 = User.objects.filter(id=pk).first()
    c = Cibling.objects.filter(cibling_2=user2,status=False)

    if not c:
        messages.error(request, 'Wrong cibling request')
    else:
        c.update(status=True)
        messages.success(request, 'Cibling accepted {}'.format(user2.first_name+' '+user2.last_name))

    return redirect('newsfeed')


@login_required
def timeline_ciblings(request,pk):
    user = User.objects.filter(id=pk).first()
    ciblings_1 = Cibling.objects.filter(cibling_1=user, status=True)
    ciblings_2 = Cibling.objects.filter(cibling_2=user, status=True)
    user_ciblings =[]

    for cibling in ciblings_1:
        user_ciblings.append(cibling.cibling_2)
    for cibling in ciblings_2:
        user_ciblings.append(cibling.cibling_1)

    count = len(user_ciblings)
    count = count//3+1


    users=[]

    for i in range(count-1):
        userl=[]
        userl.append(user_ciblings[3*i])
        userl.append(user_ciblings[3*i+1])
        userl.append(user_ciblings[3*i+2])
        users.append(userl)

    for i in range((count-1)*3, len(user_ciblings)):
        userl=[]
        userl.append(user_ciblings[i])
        users.append(userl)


    #users=[users]
    context={
        'pk': pk,
        'user': user,
        'user_ciblings': user_ciblings,
        'count': count,
        'users': users,
        'title': '{fname} {lname} Ciblings'.format(fname=user.first_name, lname=user.last_name)
    }

    return render(request, 'cibling_web/timeline_profile_ciblings.html', context)


def about(request):
    return render(request, 'cibling_web/about.html')

@login_required
def cibling_request(request):
    user = request.user

    ciblings_1 = Cibling.objects.filter(cibling_1=user, status=False)
    ciblings_2 = Cibling.objects.filter(cibling_2=user, status=False)
    user_ciblings =[]

    for cibling in ciblings_1:
        user_ciblings.append(cibling.cibling_2)
    for cibling in ciblings_2:
        user_ciblings.append(cibling.cibling_1)

    count = len(user_ciblings)
    count = count//3+1


    users=[]

    for i in range(count-1):
        userl=[]
        userl.append(user_ciblings[3*i])
        userl.append(user_ciblings[3*i+1])
        userl.append(user_ciblings[3*i+2])
        users.append(userl)

    for i in range((count-1)*3, len(user_ciblings)):
        userl=[]
        userl.append(user_ciblings[i])
        users.append(userl)


    #users=[users]
    context={
        'pk': user.id,
        'user': user,
        'user_ciblings': user_ciblings,
        'count': count,
        'users': users,
        'title': '{fname} {lname} Cibling Requests'.format(fname=user.first_name, lname=user.last_name)
    }

    return render(request, 'cibling_web/cibling_requests.html', context)
