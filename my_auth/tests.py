from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestViews(TestCase):


    def test_duplicate_email_issue(self):
        email = "user@example.com"
        password = "BXP-Xow5oPix67NUiFXF-Oe-KdZejT"
        for i in range(10):
            password = password + str(i)
            response = self.client.post(
                reverse("account_signup"),
                {"email": email, "password1": password, "password2": password},
            )
            self.assertEqual(response.status_code, 302)

        self.assertEqual(get_user_model().objects.count(), 1)
        
    def test_signup_login_logout(self):
        email = "user@example.com"
        password = "BXP-Xow5oPix67NUiFXF-Oe-KdZejT"

        # signup
        response = self.client.post(
            reverse("account_signup"),
            {"email": email, "password1": password, "password2": password},
        )

        context = getattr(response, "context", {})
        if context and "form" in context:
            print(context["form"].errors)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home"))
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get().email, email)
        self.assertTrue(get_user_model().objects.get().check_password(password))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        # logout
        response = self.client.post(reverse("account_logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        # login
        response = self.client.post(
            reverse("account_login"), {"login": email, "password": password}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        # logout
        response = self.client.post(reverse("account_logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        # login with wrong password
        response = self.client.post(
            reverse("account_login"), {"login": email, "password": "wrong"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTrue("The email address and/or password you specified are not correct." in str(getattr(response, "context", {}).get("form").errors))

        # login with wrong email
        response = self.client.post(
            reverse("account_login"), {"login": "wrong@example.com", "password": password}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTrue("The email address and/or password you specified are not correct." in str(getattr(response, "context", {}).get("form").errors))

        # sign up with already used email
        response = self.client.post(
            reverse("account_signup"),
            {"email": email, "password1": password, "password2": password},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home"))
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTrue("A user is already registered with this email address." in str(getattr(response, "context", {}).get("form").errors))