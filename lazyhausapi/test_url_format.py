
from django.test import TestCase
from django.urls import get_resolver, RegexURLResolver, RegexURLPattern


class URLFormatTest(TestCase):
    def assertUrlInvalid(self, value, url):
        assert value, "URL {} is invalid.".format(url)

    def test_url_format(self):
        self.all_urls_terminated(get_resolver())

    def all_urls_terminated(self, node, url=''):
        if isinstance(node, RegexURLResolver):
            self.assertUrlInvalid(node.regex.pattern.startswith('^'), url)
            url += node.regex.pattern[1:]
            self.all_urls_terminated(node.url_patterns, url)
        elif isinstance(node, RegexURLPattern):
            self.assertUrlInvalid(node.regex.pattern.startswith('^'), url)
            url += node.regex.pattern[1:]
            self.assertUrlInvalid(url.endswith('/$'), url)
        else:
            for pattern in node:
                self.all_urls_terminated(pattern, url)
