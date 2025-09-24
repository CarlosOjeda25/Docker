from django.test import TestCase

# users/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class ProfileSignalsTest(TestCase):
    def test_profile_created_on_user_create(self):
        """Al crear un User, debe crearse automáticamente su Profile."""
        u = User.objects.create_user(username="testuser", email="t@example.com", password="testpass123")
        # refrescar desde la BD y comprobar
        self.assertTrue(Profile.objects.filter(user=u).exists())
        profile = Profile.objects.get(user=u)
        self.assertEqual(profile.user.username, "testuser")

    def test_profile_created_on_superuser_create(self):
        """Al crear un superuser también debe crearse el Profile."""
        su = User.objects.create_superuser(username="admin", email="admin@example.com", password="adminpass123")
        self.assertTrue(Profile.objects.filter(user=su).exists())
        profile = Profile.objects.get(user=su)
        self.assertEqual(profile.user.is_superuser, True)

    def test_no_duplicate_profile_on_user_save(self):
        """Guardar el mismo User varias veces no debe crear perfiles duplicados."""
        u = User.objects.create_user(username="dupuser", email="dup@example.com", password="dup12345")
        # Guardar el usuario otra vez (simula actualizaciones)
        u.first_name = "Nombre"
        u.save()
        profiles = Profile.objects.filter(user=u)
        self.assertEqual(profiles.count(), 1)

