from django.shortcuts import render, redirect
from .models import Post,Comment
from django.contrib.auth.models import User
from django.contrib import messages
from users.models import Profile, ProfileInfo, Cibling, Institute, Expertise, Country, Subject
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from .models import Post, Activity
from django.db import models
from .forms import PostForm, CommentForm, CountryForm
from . import forms
from django.contrib.auth.decorators import login_required
from django.db.models import Q


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

def post_detail_view(request, pk):
    if request.method!='POST':
        post = Post.objects.filter(id = pk).first()
        comments = Comment.objects.filter(post=post)
        comment_form = CommentForm()
        context = {
            'user': request.user,
            'post': post,
            'comments': comments,
            'comment_form': comment_form
        }

        return render(request, 'cibling_web/post_detail.html', context)
    else:
        form = CommentForm(request.POST)
        postid = int(request.POST.get('submit'))

        if form.is_valid():
            comment = form.save(commit=False)
            post = Post.objects.filter(id=postid).first()
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('newsfeed')
        else:
            return redirect('newsfeed')


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

def getFeedPosts(request):
    return []

@login_required
def Newsfeed(request):
    if request.method!='POST':
        form = PostForm()
        comment_form = CommentForm()
        user = request.user

        ciblings_1 = Cibling.objects.filter(cibling_1=user, status=True)
        ciblings_2 = Cibling.objects.filter(cibling_2=user, status=True)
        user_ciblings = []

        for cibling in ciblings_1:
            user_ciblings.append(cibling.cibling_2)
        for cibling in ciblings_2:
            user_ciblings.append(cibling.cibling_1)

        user_ciblings = list(set(user_ciblings))
        user_ciblings.append(user)
        posts=[]

        posts_all=Post.objects.all().order_by('-time_posted')
        for post in posts_all:
            if post.author in user_ciblings:
                posts.append(post)
        '''
        for userc in user_ciblings:
            postc=Post.objects.filter(author=userc).all()
            for post in postc:
                posts.append(post)
        '''


        #posts=Post.objects.all()
        comments=Comment.objects.all()

        context={
            'posts':posts,
            'comments':comments,
            'user': request.user,
            'user_ciblings': user_ciblings[:-1],
            'number_of_ciblings': len(user_ciblings)-1,
            'form': form,
            'comment_form': comment_form,
            'title': 'Newsfeed',
            'cib_sug': right_sidebar_cibling_suggestion(request,request.user.id)
        }

        return render(request, 'cibling_web/newsfeed.html', context)
    else:
        if request.POST.get('submit')=='post-submit':
            form = PostForm(request.POST, request.FILES)

            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                #image = form.cleaned_data.get('image')
                #post.image = image
                post.save()
                return redirect('post-detail-view', pk=post.id)
            else:
                return redirect('newsfeed')
        else:
            form = CommentForm(request.POST)
            postid = int(request.POST.get('submit'))

            if form.is_valid():
                comment = form.save(commit=False)
                post = Post.objects.filter(id=postid).first()
                comment.author = request.user
                comment.post = post
                comment.save()
                return redirect('newsfeed')
            else:
                return redirect('newsfeed')

@login_required
def timeline_profile(request, pk):
    if request.method!='POST':
        if cibling_status(request, pk)!=1 and cibling_status(request, pk)!=-2:
            return timeline_profile_about(request,pk)

        form = PostForm()
        comment_form = CommentForm()
        posts=Post.objects.all().order_by('-time_posted')
        comments=Comment.objects.all()
        user=User.objects.filter(id=pk).first()

        if request.user.id == pk:
            activities_all = Activity.objects.all()
            activities = []

            for activity in activities_all:
                usera = activity.actor
                if cibling_status(request, usera.id) == 1:
                    activities.append(activity)
        else:

            activities = Activity.objects.filter(actor=user)

        context={
            'posts':posts,
            'comments':comments,
            'user': User.objects.filter(id=pk).first(),
            'form': form,
            'comment_form': comment_form,
            'pk': pk,
            'title': '{fname} {lname} Profile'.format(fname=user.first_name, lname=user.last_name),
            'addability': addability(request, pk),
            'cibling_status': cibling_status(request,pk),
            'activities': activities
        }

        return render(request, 'cibling_web/timeline_profile.html', context)

    else:
        if request.POST.get('submit') == 'post-submit':
            form = PostForm(request.POST, request.FILES)

            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()

                #needs to be fixed
                return redirect('post-detail-view', pk=post.id)
        else:
            form = CommentForm(request.POST)
            postid = int(request.POST.get('submit'))

            if form.is_valid():
                comment = form.save(commit=False)
                post = Post.objects.filter(id=postid).first()
                comment.author = request.user
                comment.post = post
                comment.save()
                return redirect('post-detail-view', pk=post.id)
            else:
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
        'title': '{fname} {lname} Profile Info'.format(fname=user.first_name, lname=user.last_name),
        'addability': addability(request, pk),

        'cibling_status': cibling_status(request, pk),
        'activities': Activity.objects.filter(actor=user)
    }
    return render(request, 'cibling_web/timeline_profile_about.html', context)

def delete_comment(request, pk):
    comment = Comment.objects.filter(id=pk).first()
    post = Post.objects.filter(id=comment.post.id).first()
    Comment.objects.filter(id=pk).delete()
    messages.success(request,'Comment deleted')
    return redirect('post-detail-view', pk=post.id)

def addability(request, pk):
    user2 = User.objects.filter(id=pk).first()
    user1 = request.user

    if user2==user1:
        return False


    ciblings_1 = Cibling.objects.filter(cibling_1=user1, cibling_2=user2)
    ciblings_2 = Cibling.objects.filter(cibling_1=user2, cibling_2=user1)
    user_ciblings = []

    for cibling in ciblings_1:
        user_ciblings.append(cibling.cibling_2)
    for cibling in ciblings_2:
        user_ciblings.append(cibling.cibling_1)

    if len(user_ciblings)!=0:
        return False
    return True

def cibling_status(request, pk):
    user2 = User.objects.filter(id=pk).first()
    user1 = request.user

    if user2 == user1:
        return -2
    ciblings_1 = Cibling.objects.filter(cibling_1=user1, cibling_2=user2)
    ciblings_2 = Cibling.objects.filter(cibling_1=user2, cibling_2=user1)
    user_ciblings = []

    for cibling in ciblings_1:
        user_ciblings.append(cibling)
    for cibling in ciblings_2:
        user_ciblings.append(cibling)

    if len(user_ciblings) == 0:
        return -1

    userc = user_ciblings[0]
    if userc.status==False:
        return 0
    else:
        return 1


@login_required
def add_cibling(request, pk):
    user2 = User.objects.filter(id=pk).first()
    user1 = request.user
    if addability(request,pk)==False:
        messages.error(request,"Wrong add request")
        return redirect('newsfeed')
    c = Cibling.objects.create(cibling_1=user1, cibling_2=user2)
    c.save()

    messages.success(request, 'Cibling request sent to {}'.format(user2.first_name+' '+user2.last_name))
    return redirect('timeline-profile',pk=user2.id)

@login_required
def accept_cibling(request, pk):
    user2 = User.objects.filter(id=pk).first()
    c = Cibling.objects.filter(cibling_1=user2,status=False)

    if not c:
        messages.error(request, 'Wrong cibling request')
    else:
        c.update(status=True)
        messages.success(request, 'Cibling accepted {}'.format(user2.first_name+' '+user2.last_name))

        return redirect('timeline-profile', pk=user2.id)


def timeline_album(request, pk):
    user = User.objects.filter(id=pk).first()
    posts_col = Post.objects.filter(author=user).order_by('-time_posted')

    posts=[]
    for post in posts_col:
        posts.append(post)


    context={
        'posts': posts,
        'user': user,
        'pk': pk,
    }

    return render(request, 'cibling_web/timeline-profile-album.html', context)


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
    count = count//3

    if count!=0:
        users1 = user_ciblings[:count]
        users2 = user_ciblings[count:2 * count]
        users3 = user_ciblings[2 * count:3 * count]
    else:
        users1=[]
        users2 = []
        users3 = []


    if len(user_ciblings)%3==1:
        users1.append(user_ciblings[-1])
    elif len(user_ciblings)%3==2:
        users1.append(user_ciblings[-1])
        users2.append(user_ciblings[-2])




    '''
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
        
    '''
    activities = Activity.objects.filter(actor=user)

    #users=[users]
    context={
        'pk': pk,
        'user': user,
        'user_ciblings': user_ciblings,
        'count': count,
        #'users': users,
        'users1': users1,
        'users2': users2,
        'users3': users3,
        'title': '{fname} {lname} Ciblings'.format(fname=user.first_name, lname=user.last_name),
        'addability': addability(request,pk),
        'cibling_status': cibling_status(request,pk),

        'activities': activities
    }

    return render(request, 'cibling_web/timeline_profile_ciblings.html', context)


def about(request):
    return render(request, 'cibling_web/about.html')

@login_required
def cibling_request(request):
    user = request.user

    #ciblings_1 = Cibling.objects.filter(cibling_1=user, status=False)
    ciblings_2 = Cibling.objects.filter(cibling_2=user, status=False)
    user_ciblings =[]

    '''
    for cibling in ciblings_1:
        user_ciblings.append(cibling.cibling_2)
    '''
    for cibling in ciblings_2:
        user_ciblings.append(cibling.cibling_1)

    count = len(user_ciblings)
    count = count//3


    if count!=0:
        users1 = user_ciblings[:count]
        users2 = user_ciblings[count:2 * count]
        users3 = user_ciblings[2 * count:3 * count]
    else:
        users1=[]
        users2 = []
        users3 = []

    if len(user_ciblings) % 3 == 1:
        users1.append(user_ciblings[-1])
    elif len(user_ciblings) % 3 == 2:
        users1.append(user_ciblings[-1])
        users2.append(user_ciblings[-2])


    #users=[users]
    context={
        'pk': user.id,
        'user': user,
        'user_ciblings': user_ciblings,
        'count': count,
        'users1': users1,
        'users2': users2,
        'users3': users3,

        'title': '{fname} {lname} Cibling Requests'.format(fname=user.first_name, lname=user.last_name),

        'activities': Activity.objects.filter(actor=user)
    }

    return render(request, 'cibling_web/cibling_requests.html', context)

def get_ciblings_by_country(request, country):
    user=request.user
    users = []
    dict = {}
    # profiles_by_institutes = []
    # profileinfos_by_subjects = []
    key = None
    institutes = Institute.objects.filter(country=country)
    for institute in institutes:
        profiles_by_countrys = Profile.objects.filter(institute=institute).exclude(user=user)
        for profile in profiles_by_countrys:
            users.append(profile.user)
            dict[profile.user.id] = country
    key = country
    return (users, dict, key)

def get_ciblings_by_univ(request, univ):
    user = request.user
    users = []
    dict = {}
    # profiles_by_institutes = []
    # profileinfos_by_subjects = []
    key = None
    profiles_by_institutes = Profile.objects.filter(institute=univ).exclude(user=user)
    for profile in profiles_by_institutes:
        users.append(profile.user)
        dict[profile.user.id] = univ
    key = univ

    return (users, dict, key)

def get_ciblings_by_subject(request, subject):
    user=request.user
    users = []
    dict = {}
    key = None
    profileinfos_by_subjects = ProfileInfo.objects.filter(subject=subject).exclude(profile=user.profile)
    for profileinfo in profileinfos_by_subjects:
        users.append(profileinfo.profile.user)
        dict[profileinfo.profile.user.id]=subject
    key = subject

    return (users, dict, key)

def get_ciblings_by_expertise(request, expertise):
    user=request.user
    users = []
    dict = {}
    key = None
    profileinfos_by_expertises = expertise.profiles.all()
    for profileinfo in profileinfos_by_expertises:
        if profileinfo.profile.user != user:
            users.append(profileinfo.profile.user)
            dict[profileinfo.profile.user.id] = expertise
    key = expertise

    return (users, dict, key)

def get_ciblings_by_key(request, univ, sub, country, exp):
    user = request.user
    users=[]
    dict={}
    #profiles_by_institutes = []
    #profileinfos_by_subjects = []
    key = None
    if univ==1:
        profiles_by_institutes = Profile.objects.filter(institute=user.profile.institute).exclude(user=user)
        for profile in profiles_by_institutes:
            users.append(profile.user)
            dict[profile.user.id]=user.profile.institute
        key = user.profile.institute
    if sub==1:
        profileinfos_by_subjects = ProfileInfo.objects.filter(subject=user.profile.profileinfo.subject).exclude(profile=user.profile)
        for profileinfo in profileinfos_by_subjects:
            users.append(profileinfo.profile.user)
            dict[profileinfo.profile.user.id]=user.profile.profileinfo.subject
        key = user.profile.profileinfo.subject
    if country==1:
        institutes = Institute.objects.filter(country=user.profile.institute.country)
        for institute in institutes:
            profiles_by_countrys = Profile.objects.filter(institute=institute).exclude(user=user)
            for profile in profiles_by_countrys:
                users.append(profile.user)
                dict[profile.user.id]=user.profile.institute.country
        key = user.profile.institute.country
    if exp==1:
        expertises = user.profile.profileinfo.expertises.all()
        for expertise in expertises:
            profileinfos_by_expertises = expertise.profiles.all()
            for profileinfo in profileinfos_by_expertises:
                if profileinfo.profile.user!=user:
                    users.append(profileinfo.profile.user)
                    dict[profileinfo.profile.user.id]=expertise
                    key = expertise
    return (users, dict, key)


def right_sidebar_cibling_suggestion(request,pk):
    (users, dict, key) = get_ciblings_by_key(request, 1, 1, 1, 1)
    users= list(set(users))

    user_ciblings = []

    for userc in users:
        if cibling_status(request, userc.id) == 0 or cibling_status(request, userc.id) == -1:
            user_ciblings.append(userc)
    if len(user_ciblings)>10:
        return user_ciblings[:10]
    else:
        return  user_ciblings

#just a comment

@login_required
def find_ciblings(request, pk):
    user = request.user
    expertise = pk % 1000
    pk = pk // 10
    country = pk % 100
    pk = pk // 10
    sub = pk % 10
    pk = pk // 10
    univ = pk

    context2 = {}

    if request.method != 'POST':
        country_form = CountryForm()
        subject_form = forms.SubjectForm()
        institute_form = forms.InstituteForm()
        expertise_form = forms.ExpertiseForm()
        if expertise == 1:
            context2['expertise_form'] = expertise_form
        if sub == 1:
            context2['subject_form'] = subject_form
        if univ == 1:
            context2['institute_form'] = institute_form
        if country == 1:
            context2['country_form'] = country_form
        (users, dict, key) =get_ciblings_by_key(request, univ,sub,country,expertise)

    else:
        if request.POST.get('submit')=='country':
            country_form = CountryForm(request.POST)
            institute_form = forms.InstituteForm()
            subject_form = forms.SubjectForm()
            expertise_form = forms.ExpertiseForm()
            context2['country_form'] = country_form
            if country_form.is_valid():
                country = country_form.cleaned_data.get('choose_country')
                (users, dict, key) = get_ciblings_by_country(request, country)
        elif request.POST.get('submit')=='institute':
            country_form = CountryForm()
            institute_form = forms.InstituteForm(request.POST)
            subject_form = forms.SubjectForm()
            expertise_form = forms.ExpertiseForm()
            context2['institute_form'] = institute_form
            if institute_form.is_valid():
                institute = institute_form.cleaned_data.get('choose_institute')
                (users, dict, key) = get_ciblings_by_univ(request, institute)
            else:
                return redirect('newsfeed')
        elif request.POST.get('submit')=='subject':
            country_form = CountryForm()
            institute_form = forms.InstituteForm()
            subject_form = forms.SubjectForm(request.POST)
            expertise_form = forms.ExpertiseForm()
            context2['subject_form'] = subject_form
            if subject_form.is_valid():
                subject = subject_form.cleaned_data.get('choose_subject')
                (users, dict, key) = get_ciblings_by_subject(request, subject)
            else:
                return redirect('newsfeed')
        elif request.POST.get('submit')=='expertise':
            country_form = CountryForm()
            institute_form = forms.InstituteForm()
            subject_form = forms.SubjectForm()
            expertise_form = forms.ExpertiseForm(request.POST)
            context2['expertise_form'] = expertise_form
            if expertise_form.is_valid():
                expertise = expertise_form.cleaned_data.get('choose_expertise')
                (users, dict, key) = get_ciblings_by_expertise(request, expertise)
            else:
                return redirect('newsfeed')

    user_ciblings = []

    for userc in users:
        if cibling_status(request, userc.id)==0 or cibling_status(request, userc.id)==-1:
            user_ciblings.append(userc)

    count = len(user_ciblings)
    count = count//3

    if count!=0:
        users1 = user_ciblings[:count]
        users2 = user_ciblings[count:2 * count]
        users3 = user_ciblings[2 * count:3 * count]
    else:
        users1=[]
        users2 = []
        users3 = []


    if len(user_ciblings)%3==1:
        users1.append(user_ciblings[-1])
    elif len(user_ciblings)%3==2:
        users1.append(user_ciblings[-1])
        users2.append(user_ciblings[-2])


    context={
        'users1': users1,
        'users2': users2,
        'users3': users3,
        'dict': dict,
        'title': 'Find Ciblings',
        'user': request.user,
        'pk': request.user.id,
        #'country_form': country_form,
        #'institute_form': institute_form,
        #'subject_form': subject_form,
        #'expertise_form': expertise_form,
        'key': key

    }

    for key in context2.keys():
        context[key] = context2[key]

    return render(request, 'cibling_web/find_ciblings.html', context)



def search_result(request):
    pk=request.GET.get('q')
    posts = Post.objects.filter(content__icontains=pk)
    '''
    users = User.objects.annotate(
        search=search.SearchVector('first_name','last_name'),
    ).filter(search=pk)
    '''
    users11 = User.objects.filter(first_name__icontains=pk)
    users22 = User.objects.filter(last_name__icontains=pk)

    user_ins = User.objects.filter(profile__institute__institute__icontains=pk)

    (user_ins1, user_ins2, user_ins3) = three_splitter(list(user_ins))

    user_couns = []
    countries = Country.objects.filter(country__icontains=pk)
    for country in countries:
        users_temp = User.objects.filter(profile__institute__country_id=country.id)
        for user in users_temp:
            user_couns.append(user)

    (user_couns1, user_couns2, user_couns3) = three_splitter(user_couns)

    user_exps = []
    expertises = Expertise.objects.filter(expertise__icontains=pk)
    for expertise in expertises:
        users_temp = User.objects.filter(profile__profileinfo__expertises__exact=expertise)
        for user in users_temp:
            user_exps.append(user)

    (user_exps1, user_exps2, user_exps3) = three_splitter(user_exps)

    user_subs = []
    subjects = Subject.objects.filter(subject__icontains=pk)
    for sub in subjects:
        users_temp = User.objects.filter(profile__profileinfo__subject__exact=sub)
        for user in users_temp:
            user_subs.append(user)

    (user_subs1, user_subs2, user_subs3) = three_splitter(user_subs)


    user_ciblings=[]
    for user in users22:
        user_ciblings.append(user)
    for user in users11:
        if user not in user_ciblings:
            user_ciblings.append(user)

    count = len(user_ciblings)
    count = count//3

    if count!=0:
        users1 = user_ciblings[:count]
        users2 = user_ciblings[count:2 * count]
        users3 = user_ciblings[2 * count:3 * count]
    else:
        users1=[]
        users2 = []
        users3 = []


    if len(user_ciblings)%3==1:
        users1.append(user_ciblings[-1])
    elif len(user_ciblings)%3==2:
        users1.append(user_ciblings[-1])
        users2.append(user_ciblings[-2])

    context={
        'pk': pk,
        'posts': posts,
        #'users': users,
        'title': 'Search Result',
        'users1': users1,
        'users2': users2,
        'users3': users3,
        'userins1': user_ins1,
        'userins2': user_ins2,
        'userins3': user_ins3,
        'usercouns1': user_couns1,
        'usercouns2': user_couns2,
        'usercouns3': user_couns3,
        'userexps1': user_exps1,
        'userexps2': user_exps2,
        'userexps3': user_exps3,
        'usersubs1': user_subs1,
        'usersubs2': user_subs2,
        'usersubs3': user_subs3,
    }

    return render(request, 'cibling_web/search_result.html', context)


def three_splitter(users):
    user_ciblings=users

    count = len(user_ciblings)
    count = count//3

    if count!=0:
        users1 = user_ciblings[:count]
        users2 = user_ciblings[count:2 * count]
        users3 = user_ciblings[2 * count:3 * count]
    else:
        users1=[]
        users2 = []
        users3 = []


    if len(user_ciblings)%3==1:
        users1.append(user_ciblings[-1])
    elif len(user_ciblings)%3==2:
        users1.append(user_ciblings[-1])
        users2.append(user_ciblings[-2])

    return (users1, users2, users3)