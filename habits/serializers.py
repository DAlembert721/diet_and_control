from rest_framework import serializers

from habits.models import PhysicalActivity, HarmfulHabit


class PhysicalActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalActivity
        fields = ('id', 'name', 'description',)


class HarmfulHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = HarmfulHabit
        fields = ('id', 'name', 'description')
