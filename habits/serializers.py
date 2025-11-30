from rest_framework import serializers
from .models import Habit
from .validators import validate_habit
from django.core.exceptions import ValidationError


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user", "created_at")

    def validate(self, data):
        # Создаем временный объект для валидации
        if self.instance:
            habit = self.instance
            for attr, value in data.items():
                setattr(habit, attr, value)
        else:
            habit = Habit(**data)
            habit.user = self.context["request"].user

        try:
            validate_habit(habit)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return data

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
