from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from cibling_web.forms import PostForm
from users.models import Cibling
from .views import right_sidebar_cibling_suggestion

from django.db.models import Q


class NewsFeedView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = PostForm()
        user = request.user
        ciblings_1 = Cibling.objects.filter(cibling_1=user, status=True)
        ciblings_2 = Cibling.objects.filter(cibling_2=user, status=True)
        user_ciblings = []

        for cibling in ciblings_1:
            user_ciblings.append(cibling.cibling_2)
        for cibling in ciblings_2:
            user_ciblings.append(cibling.cibling_1)

        user_ciblings = list(set(user_ciblings))[:30]

        context={
            "user":user,
            "user_ciblings" : user_ciblings,
            'number_of_ciblings': len(user_ciblings) - 1,
            'cib_sug': right_sidebar_cibling_suggestion(request, request.user.id),
            'form': form,
        }

        return render(request, "cibling_web/newsfeed-scrollable.html", context)

    def post(self, request):
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # image = form.cleaned_data.get('image')
            # post.image = image
            post.save()
            return redirect('post-detail-view', pk=post.id)
        else:
            return redirect('newsfeed')



