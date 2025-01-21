from rest_framework import serializers
from .models import Score
from enums.level_type import LevelType

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'

class ScoreDataChartSerializer(serializers.Serializer):
    level1 = serializers.IntegerField()
    level2 = serializers.IntegerField()
    level3 = serializers.IntegerField()
    level4 = serializers.IntegerField()
    total = serializers.IntegerField()
    chart_type = serializers.CharField()
    values= serializers.ListField(child=serializers.FloatField())
    labels = serializers.ListField(child=serializers.CharField())

    def to_representation(self, instance):
        chart_type = instance['chart_type']

        if chart_type == 'bar':
            return {
                'values': [instance['level1'], instance['level2'], instance['level3'], instance['level4']],
                'labels': [LevelType.LEVEL1.value, LevelType.LEVEL2.value, LevelType.LEVEL3.value, LevelType.LEVEL4.value]
            }
        else:  
            total = instance['total']
            if total == 0:
                return {
                    'values': [0, 0, 0, 0],
                    'labels': [LevelType.LEVEL1.value, LevelType.LEVEL2.value, LevelType.LEVEL3.value, LevelType.LEVEL4.value]
                }

            level1_percentage = round((instance['level1'] / total) * 100, 2)
            level2_percentage = round((instance['level2'] / total) * 100, 2)
            level3_percentage = round((instance['level3'] / total) * 100, 2)
            level4_percentage = round(100 - (level1_percentage + level2_percentage + level3_percentage), 2)

            return {
                'values': [level1_percentage, level2_percentage, level3_percentage, level4_percentage],
                'labels': [LevelType.LEVEL1.value, LevelType.LEVEL2.value, LevelType.LEVEL3.value, LevelType.LEVEL4.value]
            }