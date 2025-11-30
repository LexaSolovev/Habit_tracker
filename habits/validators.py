from django.core.exceptions import ValidationError


def validate_habit(habit):
    errors = {}

    # Исключить одновременный выбор связанной привычки и вознаграждения
    if habit.related_habit and habit.reward:
        errors["reward"] = (
            "Нельзя одновременно указывать связанную привычку и вознаграждение"
        )
        errors["related_habit"] = (
            "Нельзя одновременно указывать связанную привычку и вознаграждение"
        )

    # Время выполнения должно быть не больше 120 секунд
    if habit.estimated_duration > 120:
        errors["estimated_duration"] = "Время выполнения не должно превышать 120 секунд"

    # В связанные привычки могут попадать только привычки с признаком приятной привычки
    if habit.related_habit and not habit.related_habit.is_pleasant:
        errors["related_habit"] = "Связанная привычка должна быть приятной"

    # У приятной привычки не может быть вознаграждения или связанной привычки
    if habit.is_pleasant:
        if habit.reward:
            errors["reward"] = "У приятной привычки не может быть вознаграждения"
        if habit.related_habit:
            errors["related_habit"] = (
                "У приятной привычки не может быть связанной привычки"
            )

    # Нельзя выполнять привычку реже, чем 1 раз в 7 дней
    if habit.frequency not in ["daily", "weekly"]:
        errors["frequency"] = 'Периодичность должна быть "ежедневно" или "еженедельно"'

    if errors:
        raise ValidationError(errors)
