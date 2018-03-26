from django.urls import path

from . import views

app_name = 'lotto'
urlpatterns = [
    path('', views.lotto_analysis_home, name='lotto-home'),
    path('number-frequencies/', views.get_number_frequency, name='number-frequency'),
    path('search-draw/', views.search_results_number_draw, name='search-draw'),
]
