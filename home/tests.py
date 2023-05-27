from django.test import TestCase

class HomePageTest(TestCase):
    def test_view_response(self):
        print("Test home page")
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/landing_page.html')
        title = response.context["title"]
        expected_title = "Home"
        self.assertEqual(title, expected_title)

class LearnPageTest(TestCase):
    def test_view_response(self):
        print("Test learn page")
        response = self.client.get('/learn/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/learn_page.html')
        title = response.context["title"]
        expected_title = "Learn"
        self.assertEqual(title, expected_title)

class ContactPageTest(TestCase):
    def test_view_response(self):
        print("Test contact page")
        response = self.client.get('/contact-us/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/contact_us_page.html')
        title = response.context["title"]
        expected_title = "Contact Us"
        self.assertEqual(title, expected_title)

class AboutPageTest(TestCase):
    def test_view_response(self):
        print("Test about page")
        response = self.client.get('/about-us/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/about_us_page.html')
        title = response.context["title"]
        expected_title = "About Us"
        self.assertEqual(title, expected_title)

class DocumentationPageTest(TestCase):
    def test_view_response(self):
        print("Test documentation page")
        response = self.client.get('/documentation/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/documentation_page.html')
        title = response.context["title"]
        expected_title = "API Documentation"
        self.assertEqual(title, expected_title)

class NotFoundPageTest(TestCase):
    def test_view_response(self):
        print("Test not found page")
        response = self.client.get('/notfound/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
        title = response.context["title"]
        expected_title = "Page not found"
        self.assertEqual(title, expected_title)
