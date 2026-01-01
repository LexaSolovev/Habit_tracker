from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Habit
from .serializers import HabitSerializer
from .pagination import HabitPagination


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_pleasant", "is_public"]

    def get_queryset(self):
        if self.action == "public":
            return Habit.objects.filter(is_public=True)
        return Habit.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action == "public":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=["get"])
    def public(self, request):
        habits = self.get_queryset()
        page = self.paginate_queryset(habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(habits, many=True)
        return Response(serializer.data)
