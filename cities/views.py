from typing import List
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.db.models import Q 

from .models import City
# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'

class SearchResultView(ListView):
    model = City
    template_name = 'search_result.html'
    # queryset = City.objects.filter(name__icontains='Miami')
    

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list= City.objects.filter(
            Q(name__icontains=query) | Q(state__icontains=query)
        )
        return object_list