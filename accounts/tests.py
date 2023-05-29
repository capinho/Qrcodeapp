import random
from string import ascii_letters, digits
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


class AccountsViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("accounts:register-page")
        self.login_url = reverse("accounts:login-page")
        self.dashboard_url = reverse("qrgen:dashboard")
        self.homepage_url = reverse("home:home-page")
        self.user_credentials = {
            "fname": "John",
            "lname": "Doe",
            "email": "johndoe@example.com",
            "pswrd": "password",
        }
        User.objects.create_user(
            username=self.user_credentials["email"],
            email=self.user_credentials["email"],
            password=self.user_credentials["pswrd"],
        )

    def test_register_view_authenticated_user(self):
        # Vérifie si un utilisateur déjà authentifié est redirigé depuis la vue d'inscription
        self.client.login(
            username=self.user_credentials["email"],
            password=self.user_credentials["pswrd"],
        )
        response = self.client.get(self.register_url)
        self.assertRedirects(response, self.dashboard_url)

    def test_register_view_post_request_existing_email(self):
        # Vérifie si un message d'erreur est renvoyé lorsque l'adresse e-mail existe déjà lors d'une requête POST
        response = self.client.post(self.register_url, self.user_credentials)
        self.assertContains(
            response, "Email address already exists, register a new email address"
        )

    def test_register_view_post_request_new_user(self):
        # Vérifie si un nouvel utilisateur est créé avec succès lors d'une requête POST
        new_user_credentials = {
            "fname": "Jane",
            "lname": "Smith",
            "email": "janesmith@example.com",
            "pswrd": "password123",
        }
        response = self.client.post(
            self.register_url, new_user_credentials, follow=True
        )
        self.assertRedirects(response, self.dashboard_url)
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, "Welcome to the dashboard")

    def test_login_view_authenticated_user(self):
        # Vérifie si un utilisateur déjà authentifié est redirigé depuis la vue de connexion
        self.client.login(
            username=self.user_credentials["email"],
            password=self.user_credentials["pswrd"],
        )
        response = self.client.get(self.login_url)
        self.assertRedirects(response, self.dashboard_url)

    def test_login_view_post_request_valid_credentials(self):
        # Vérifie si un utilisateur peut se connecter avec des identifiants valides
        response = self.client.post(self.login_url, self.user_credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0], reverse("qrgen:dashboard"))

    def test_login_view_post_request_invalid_credentials(self):
        # Vérifie si un message d'erreur est renvoyé lorsque des identifiants invalides sont utilisés lors d'une requête POST
        invalid_credentials = {"email": "johndoe@example.com", "pswrd": "wrongpassword"}
        response = self.client.post(self.login_url, invalid_credentials)
        self.assertContains(response, "Email Address and Password do not exist")

    def test_logout_view(self):
        # Vérifie si un utilisateur peut se déconnecter avec succès
        self.client.login(
            username=self.user_credentials["email"],
            password=self.user_credentials["pswrd"],
        )
        response = self.client.get(reverse("accounts:logout"))
        self.assertRedirects(response, self.homepage_url)

    def test_monkey_create_user(self):
        def generate_random_data():
            random_name = ''.join(random.choice(ascii_letters) for _ in range(10))
            random_email = ''.join(random.choice(ascii_letters) for _ in range(10)) + '@example.com'
            random_pwd = ''.join(random.choice(ascii_letters + digits) for _ in range(12))
            return { "fname": 'Jane',
                "lname": random_name,
                "email": random_email,
                "pswrd": random_pwd
            }
        for _ in range(100):
            user_credentials = generate_random_data()
            response = self.client.post(
                self.register_url, user_credentials, follow=True
            )
            self.assertRedirects(response, self.dashboard_url)
            messages = list(response.context["messages"])
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].message, "Welcome to the dashboard")
        print("Monkey test passed")