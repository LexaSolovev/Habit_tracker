from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.exceptions import ValidationError
from .models import Habit
from .validators import validate_habit

User = get_user_model()


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="20:00:00",
            action="Принять ванну",
            is_pleasant=True,
            estimated_duration=120,
        )

    def test_create_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Читать книгу",
            estimated_duration=120,
            is_public=True,
        )
        self.assertEqual(habit.action, "Читать книгу")
        self.assertEqual(habit.user.email, "test@example.com")
        self.assertTrue(habit.is_public)

    def test_habit_str_representation(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Парк",
            time="07:00:00",
            action="Бегать",
            estimated_duration=90,
        )
        expected_str = "Бегать в 07:00:00 в Парк"
        self.assertEqual(str(habit), expected_str)

    def test_habit_clean_method_valid(self):
        habit = Habit(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Читать книгу",
            estimated_duration=120,
            reward="Выпить кофе",
        )
        # Не должно вызывать исключение
        habit.clean()

    def test_habit_clean_method_invalid(self):
        habit = Habit(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Читать книгу",
            estimated_duration=150,  # Больше 120 секунд
            reward="Выпить кофе",
        )
        with self.assertRaises(ValidationError):
            habit.clean()


class HabitValidatorTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="20:00:00",
            action="Принять ванну",
            is_pleasant=True,
            estimated_duration=120,
        )

    def test_validate_habit_both_reward_and_related_habit(self):
        habit = Habit(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Читать книгу",
            estimated_duration=120,
            reward="Выпить кофе",
            related_habit=self.pleasant_habit,
        )
        with self.assertRaises(ValidationError) as context:
            validate_habit(habit)
        self.assertIn("reward", str(context.exception))
        self.assertIn("related_habit", str(context.exception))

    def test_validate_habit_duration_exceeds_limit(self):
        habit = Habit(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Читать книгу",
            estimated_duration=150,
        )
        with self.assertRaises(ValidationError) as context:
            validate_habit(habit)
        self.assertIn("estimated_duration", str(context.exception))

    def test_validate_pleasant_habit_with_reward(self):
        habit = Habit(
            user=self.user,
            place="Дом",
            time="20:00:00",
            action="Слушать музыку",
            is_pleasant=True,
            estimated_duration=120,
            reward="Награда",
        )
        with self.assertRaises(ValidationError) as context:
            validate_habit(habit)
        self.assertIn("reward", str(context.exception))

    def test_validate_pleasant_habit_with_related_habit(self):
        another_pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="21:00:00",
            action="Смотреть фильм",
            is_pleasant=True,
            estimated_duration=120,
        )
        habit = Habit(
            user=self.user,
            place="Дом",
            time="20:00:00",
            action="Слушать музыку",
            is_pleasant=True,
            estimated_duration=120,
            related_habit=another_pleasant_habit,
        )
        with self.assertRaises(ValidationError) as context:
            validate_habit(habit)
        self.assertIn("related_habit", str(context.exception))


class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            email="other@example.com", password="otherpass123"
        )
        self.client.force_authenticate(user=self.user)

        self.habit_data = {
            "place": "Парк",
            "time": "07:00:00",
            "action": "Бегать",
            "estimated_duration": 90,
            "is_public": True,
        }

        # Создаем тестовые привычки
        self.habit = Habit.objects.create(user=self.user, **self.habit_data)
        self.private_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Читать книгу",
            estimated_duration=120,
            is_public=False,
        )
        self.other_user_habit = Habit.objects.create(
            user=self.other_user,
            place="Офис",
            time="12:00:00",
            action="Обедать",
            estimated_duration=60,
            is_public=True,
        )

    def test_create_habit(self):
        response = self.client.post("/api/habits/", self.habit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 4)  # 3 уже создано + 1 новый
        self.assertEqual(response.data["action"], "Бегать")
        self.assertEqual(response.data["user"], self.user.id)

    def test_create_habit_invalid_data(self):
        invalid_data = self.habit_data.copy()
        invalid_data["estimated_duration"] = 150  # Больше 120 секунд
        response = self.client.post("/api/habits/", invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("estimated_duration", response.data)

    def test_get_habits_list(self):
        response = self.client.get("/api/habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 2
        )  # Только привычки текущего пользователя
        self.assertEqual(response.data["results"][0]["action"], "Читать книгу")

    def test_get_public_habits_without_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/habits/public/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Должны видеть только публичные привычки
        public_habits = [h for h in response.data["results"] if h["is_public"]]
        self.assertEqual(len(public_habits), len(response.data["results"]))

    def test_get_habit_detail(self):
        response = self.client.get(f"/api/habits/{self.habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "Бегать")

    def test_update_habit(self):
        update_data = self.habit_data.copy()
        update_data["action"] = "Бегать быстро"
        response = self.client.put(f"/api/habits/{self.habit.id}/", update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Бегать быстро")

    def test_delete_habit(self):
        response = self.client.delete(f"/api/habits/{self.habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 2)

    def test_cannot_access_other_user_private_habit(self):
        response = self.client.get(f"/api/habits/{self.other_user_habit.id}/")
        # Должен получить 404, даже если привычка публичная, но не своя
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_update_other_user_habit(self):
        update_data = self.habit_data.copy()
        update_data["action"] = "Измененное действие"
        response = self.client.put(
            f"/api/habits/{self.other_user_habit.id}/", update_data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
