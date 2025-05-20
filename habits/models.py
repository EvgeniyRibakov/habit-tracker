from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Habit(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='related_habits'
    )
    periodicity = models.PositiveIntegerField(default=1)  # In days
    reward = models.CharField(max_length=255, null=True, blank=True)
    duration = models.PositiveIntegerField()  # In seconds
    is_public = models.BooleanField(default=False)

    def clean(self):
        if self.reward and self.related_habit:
            raise ValidationError("Cannot set both reward and related habit.")
        if self.duration > 120:
            raise ValidationError("Habit duration cannot exceed 120 seconds.")
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Related habit must be a pleasant habit.")
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("Pleasant habit cannot have reward or related habit.")
        if self.periodicity > 7:
            raise ValidationError("Habit periodicity cannot be less frequent than once every 7 days.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.action} at {self.time} in {self.place}"

    class Meta:
        verbose_name = "Habit"
        verbose_name_plural = "Habits"
