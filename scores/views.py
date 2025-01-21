from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Score
from .serializers import ScoreSerializer, ScoreDataChartSerializer
from django.db.models import F, Value, Count, Case, When, Sum
from django.db.models.functions import Coalesce 
from django.db.models import ExpressionWrapper, FloatField , IntegerField
from enums.group_type import GroupType
from django.core.cache import cache


@api_view(['GET'])
def check_score(request, student_id):
    score = cache.get(f"student{student_id}")

    if not score:
        try:
            score = Score.objects.get(student_id=student_id)
        except Score.DoesNotExist:
            return Response({"message": "Score not found."}, status=404)
        score = ScoreSerializer(score).data
        cache.set(f"student{student_id}", score, timeout=60*15)

    return Response(score)

@api_view(['GET'])
def get_top_10_group(request, group_type):
    top_10_group = cache.get(f"top_10_group{group_type}")
    
    if not top_10_group:
        subjects = GroupType[group_type].value
        
        total_score_expr = Coalesce(F(subjects[0]), Value(0)) + Coalesce(F(subjects[1]), Value(0)) + Coalesce(F(subjects[2]), Value(0))

        scores = Score.objects.annotate(
            total_score=ExpressionWrapper(total_score_expr, output_field=FloatField())
        ).order_by('-total_score')  

        top_10_group = scores[:10]

        top_10_group = ScoreSerializer(top_10_group, many=True).data
        cache.set(f"top_10_group{group_type}", top_10_group, timeout=60*15)

    return Response(top_10_group)


@api_view(['GET'])
def get_data_chart(request, subject, chart_type):

    chart_data = cache.get(f"chart_data_{subject}_{chart_type}")

    if not chart_data:

        score_stats = Score.objects.aggregate(
            level1=Count(Case(When(**{f'{subject}__gte': 8, f'{subject}__isnull': False}, then=Value(1)))),
            level2=Count(Case(When(**{f'{subject}__gte': 6, f'{subject}__lt': 8, f'{subject}__isnull': False}, then=Value(1)))),
            level3=Count(Case(When(**{f'{subject}__gte': 4, f'{subject}__lt': 6, f'{subject}__isnull': False}, then=Value(1)))),
            level4=Count(Case(When(**{f'{subject}__lt': 4, f'{subject}__isnull': False}, then=Value(1)))),
            total=Count(Case(When(**{f'{subject}__isnull': False}, then=Value(1))))
        )

        raw_data = {
            'level1': score_stats['level1'],
            'level2': score_stats['level2'],
            'level3': score_stats['level3'],
            'level4': score_stats['level4'],
            'total': score_stats['total'],
            "chart_type": chart_type
        }

        chart_data = ScoreDataChartSerializer(raw_data).data
        cache.set(f"chart_data_{subject}_{chart_type}", chart_data, timeout=60*15)

    return Response(chart_data)




