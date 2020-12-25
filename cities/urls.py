from django.urls import path

from .views import HomePageView, SearchResultView

urlpatterns = [
    path('search/', SearchResultView.as_view(), name='search_results'),
    path('', HomePageView.as_view(), name='home'),
]