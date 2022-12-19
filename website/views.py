
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

from website.models import ServerListing, Tag

class HomePageView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['latest_articles'] = Article.objects.all()[:5]
        return context

class ServerListings(ListView):
    model = ServerListing
    queryset = ServerListing.objects.filter(status=1).order_by('-created_on')
    template_name = 'server-list.html'
    paginate_by = 10
