
from django.urls import path
from scores.views import check_score, get_top_10_group, get_data_chart

urlpatterns = [
   path('scores/<str:student_id>/', check_score, name='check_score'),
   path('scores/top10/<str:group_type>/', get_top_10_group, name='get_top_10_group'),
   path('scores/chart/<str:chart_type>/<str:subject>/', get_data_chart, name='get_data_chart'),
]
