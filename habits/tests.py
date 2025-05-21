from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Habit, Profile
from django.utils import timezone
import datetime


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Park',
            time=datetime.time(9, 0),
            action='Morning walk',
            duration=60,
            periodicity=1,
            is_pleasant=True,
            created_at=timezone.now()
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place='Home',
            time=datetime.time(8, 0),
            action='Morning exercise',
            duration=60,
            periodicity=1,
            is_public=True,
            created_at=timezone.now()
        )

    def test_habit_creation(self):
        self.assertEqual(self.habit.action, 'Morning exercise')
        self.assertEqual(self.habit.duration, 60)

    def test_duration_validation(self):
        with self.assertRaises(Exception):
            invalid_habit = Habit(
                user=self.user,
                place='Home',
                time=datetime.time(8, 0),
                action='Invalid habit',
                duration=150
            )
            invalid_habit.full_clean()

    def test_clean_validation_reward_and_related_habit(self):
        with self.assertRaises(Exception):
            habit = Habit(
                user=self.user,
                place='Home',
                time=datetime.time(8, 0),
                action='Test habit',
                duration=60,
                periodicity=1,
                reward='Test reward',
                related_habit=self.pleasant_habit
            )
            habit.clean()

    def test_clean_validation_related_habit_not_pleasant(self):
        non_pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Gym',
            time=datetime.time(10, 0),
            action='Workout',
            duration=60,
            periodicity=1,
            is_pleasant=False,
            created_at=timezone.now()
        )
        with self.assertRaises(Exception):
            habit = Habit(
                user=self.user,
                place='Home',
                time=datetime.time(8, 0),
                action='Test habit',
                duration=60,
                periodicity=1,
                related_habit=non_pleasant_habit
            )
            habit.clean()

    def test_clean_validation_pleasant_habit_with_reward(self):
        with self.assertRaises(Exception):
            habit = Habit(
                user=self.user,
                place='Home',
                time=datetime.time(8, 0),
                action='Test habit',
                duration=60,
                periodicity=1,
                is_pleasant=True,
                reward='Test reward'
            )
            habit.clean()

    def test_clean_validation_pleasant_habit_with_related_habit(self):
        with self.assertRaises(Exception):
            habit = Habit(
                user=self.user,
                place='Home',
                time=datetime.time(8, 0),
                action='Test habit',
                duration=60,
                periodicity=1,
                is_pleasant=True,
                related_habit=self.pleasant_habit
            )
            habit.clean()

    def test_clean_validation_periodicity(self):
        with self.assertRaises(Exception):
            habit = Habit(
                user=self.user,
                place='Home',
                time=datetime.time(8, 0),
                action='Test habit',
                duration=60,
                periodicity=8
            )
            habit.clean()


class HabitAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.habit = Habit.objects.create(
            user=self.user,
            place='Home',
            time=datetime.time(8, 0),
            action='Morning exercise',
            duration=60,
            periodicity=1,
            is_public=True,
            created_at=timezone.now()
        )

    def test_create_habit(self):
        response = self.client.post('/api/habits/', {
            'place': 'Home',
            'time': '08:00',
            'action': 'Morning exercise',
            'duration': 60,
            'periodicity': 1,
            'is_public': True
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 2)

    def test_get_habit_list(self):
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)

    def test_update_habit(self):
        response = self.client.patch(f'/api/habits/{self.habit.id}/', {
            'action': 'Updated exercise',
            'duration': 90
        })
        self.assertEqual(response.status_code, 200)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, 'Updated exercise')
        self.assertEqual(self.habit.duration, 90)

    def test_delete_habit(self):
        response = self.client.delete(f'/api/habits/{self.habit.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Habit.objects.count(), 0)


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user, telegram_id='123456789')

    def test_profile_creation(self):
        self.assertEqual(self.profile.telegram_id, '123456789')
        self.assertEqual(str(self.profile), f"Profile for {self.user.username}")
