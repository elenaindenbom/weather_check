from django.test import TestCase, Client


class URLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        """Проверка доступности главной страницы"""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about_url_uses_correct_template(self):
        """Проверка шаблона для главной страницы"""
        response = self.guest_client.get('/')
        self.assertTemplateUsed(response, 'weather/index.html')
