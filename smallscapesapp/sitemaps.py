from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """
    Simple sitemap for the site's static (non-database-driven) pages.
    priority/changefreq are rough hints for search engines, not guarantees.
    """
    protocol = 'https'

    def items(self):
        return [
            ('home', 1.0, 'weekly'),
            ('about', 0.7, 'monthly'),
            ('projects', 0.9, 'weekly'),
            ('review_list', 0.8, 'weekly'),
            ('leave_review', 0.5, 'monthly'),
            ('privacy', 0.2, 'yearly'),
            ('terms', 0.2, 'yearly'),
        ]

    def location(self, item):
        name, _, _ = item
        return reverse(name)

    def priority(self, item):
        _, priority, _ = item
        return priority

    def changefreq(self, item):
        _, _, freq = item
        return freq
