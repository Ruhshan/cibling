from django.shortcuts import render
from django.views.generic import View

class FindCiblingPageView(View):
    def get(self, request):

        return render(request, "cibling_web/find_ciblings.html")