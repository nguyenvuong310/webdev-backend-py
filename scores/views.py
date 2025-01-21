from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Score
from .serializers import ScoreSerializer, ScoreDataChartSerializer
from django.db.models import F, Value, Count, Case, When, Sum
from django.db.models.functions import Coalesce 
from django.db.models import ExpressionWrapper, FloatField , IntegerField
from enums.group_type import GroupType, GroupTypeCode
from enums.level_type import LevelType
from enums.chart_type import ChartType
from enums.subject_type import SubjectType
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

level_type_example = [level.value for level in LevelType]




@swagger_auto_schema(
    method='get',
    operation_summary='Get score of student',
    manual_parameters=[
        openapi.Parameter(
            'student_id',
            openapi.IN_PATH,
            description="ID of the student to retrieve the score for",
            type=openapi.TYPE_STRING,
        ),
    ],
    responses={
        200: openapi.Response(
            description="Score retrieved successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_STRING, description="Student ID", exmaple='1000001'),
                    "math": openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        format=openapi.FORMAT_FLOAT,
                        description="Math score of the student", 
                        example= 8.0
                    ),
                    "literature": openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        format=openapi.FORMAT_FLOAT,
                        description="Literature score of the student",
                        example= 8.5
                    ),
                    "language": openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        format=openapi.FORMAT_FLOAT,
                        description="English score of the student",
                        example= 8.0
                    ),
                    "physics": openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        format=openapi.FORMAT_FLOAT,
                        description="Physics score of the student",
                        example= 8.0
                    ),
                    "chemistry": openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        format=openapi.FORMAT_FLOAT,
                        description="Chemistry score of the student",
                        example= 8.0
                    ),
                    "biology": openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        format=openapi.FORMAT_FLOAT,
                        description="Biology score of the student",
                        example= 8.0
                    ),
                    "history": openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        format=openapi.FORMAT_FLOAT,
                        description="History score of the student",
                        example= 8.0
                    ),
                    "geography": openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        format=openapi.FORMAT_FLOAT,
                        description="Geography score of the student",
                        example= 8.0
                    ),
                    "civics": openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        format=openapi.FORMAT_FLOAT,
                        description="Civic Education score of the student",
                        example= 8.0
                    ),
                    "foreign_language_code": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Foreign language code of the student",
                        example= 'N1'
                    ),

                },
            ),
        ),
    },
)

@api_view(['GET'])
def check_score(request, student_id):
    score = cache.get(f"student{student_id}")

    if not score:
        try:
            score = Score.objects.get(student_id=student_id)
        except Score.DoesNotExist:
            return Response({"message": "score with student id not found."}, status=404)
        score = ScoreSerializer(score).data
        cache.set(f"student{student_id}", score, timeout=60*15)

    return Response(score)





@swagger_auto_schema(
    method='get',
    operation_summary='Get top student of group type',
    manual_parameters=[
    openapi.Parameter(
        'group_type',
        openapi.IN_PATH,
        description="Type of group to retrieve the top 10 students",
        type=openapi.TYPE_STRING,
        enum=[group.value for group in GroupTypeCode],  
    ),
],
    responses={
        200: openapi.Response(
            description="Scores retrieved successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_STRING, description="Student ID", example='1000001'),
                        "math": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            format=openapi.FORMAT_FLOAT,
                            description="Math score of the student",
                            example=8.0,
                        ),
                        "literature": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            format=openapi.FORMAT_FLOAT,
                            description="Literature score of the student",
                            example=8.5,
                        ),
                        "language": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            format=openapi.FORMAT_FLOAT,
                            description="English score of the student",
                            example=8.0,
                        ),
                        "physics": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            format=openapi.FORMAT_FLOAT,
                            description="Physics score of the student",
                            example=8.0,
                        ),
                        "chemistry": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            format=openapi.FORMAT_FLOAT,
                            description="Chemistry score of the student",
                            example=8.0,
                        ),
                        "biology": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            format=openapi.FORMAT_FLOAT,
                            description="Biology score of the student",
                            example=8.0,
                        ),
                        "history": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            format=openapi.FORMAT_FLOAT,
                            description="History score of the student",
                            example=8.0,
                        ),
                        "geography": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            format=openapi.FORMAT_FLOAT,
                            description="Geography score of the student",
                            example=8.0,
                        ),
                        "civics": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            format=openapi.FORMAT_FLOAT,
                            description="Civic Education score of the student",
                            example=8.0,
                        ),
                        "foreign_language_code": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Foreign language code of the student",
                            example='N1',
                        ),
                    },
                ),
            ),
        ),
    },
)
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



@swagger_auto_schema(
    method='get',
    operation_summary='Get score of student',
    manual_parameters=[
        openapi.Parameter(
            'chart_type',
            openapi.IN_PATH,
            description="type of chart to retrieve the score for",
            type=openapi.TYPE_STRING,
            enum=[chart_type.value for chart_type in ChartType],
        ),
        openapi.Parameter(
            'subject',
            openapi.IN_PATH,
            description="name of subject to retrieve the score for",
            type=openapi.TYPE_STRING,
            enum=[subject.value for subject in SubjectType],
        ),
    ],
    responses={
        200: openapi.Response(
            description="Score retrieved successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "values": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="Array of student IDs or numerical values",
                    items=openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        format=openapi.FORMAT_FLOAT,
                    ),
                    example=[10, 20, 30, 40],  
    ),
                    

                "labels": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="Array of math scores or levels of the students",
                    items=openapi.Schema(
                        type=openapi.TYPE_STRING,
                    ),
                    example=level_type_example,  # Dynamically pass the example
                ),
}
            ),
        ),
    },
)

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




