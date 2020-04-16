from django.test import Client
from django.test import TestCase
from django.views.generic import TemplateView


class Test(TestCase):
    def setUp(self) -> None:
        self.cli = Client()

    def test_get(self):
        resp = self.cli.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.has_header("Cache-Control"))
        self.assertEqual(resp.get("Cache-Control"), f"max-age={60 * 60 * 24}")

        self.assertEqual(resp.resolver_match.app_name, "target")
        self.assertEqual(resp.resolver_match.url_name, "index")
        self.assertEqual(resp.resolver_match.view_name, "target:index")
        self.assertEqual(
            resp.resolver_match.func.__name__, TemplateView.as_view().__name__
        )

        self.assertEqual(resp.template_name, ["target/index.html"])
