from django.test import TestCase


class UnknownPagesTestCase(TestCase):

    def setUp(self):
        self.not_existed_endpoints = ['/test/', "/test/test/", "/historic/", "/stock/", "/stock/AAL/test/"]
        self.endpoints_to_redirect = ['/test', '/test/test', '/historic', '/stock', '/stock/AAL/test', '/login']

    def test_page_not_found(self):
        for endpoint in self.not_existed_endpoints:
            response = self.client.get(endpoint)
            self.assertTemplateUsed(response, "exception.html")
            self.assertEquals(response.status_code, 404)

    def test_page_redirect(self):
        for endpoint in self.endpoints_to_redirect:
            response = self.client.get(endpoint)
            self.assertRedirects(response, endpoint + '/', fetch_redirect_response=False)
