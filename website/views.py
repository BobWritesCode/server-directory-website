
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

from website.models import ServerListing, Tag, Game

def index(request):
    games = Game.objects.filter(status=1)
    for x in games:
        print(x.image)
    ctx = {'games': games}
    return render(request, "index.html", ctx)


class ServerListings(ListView):
    model = ServerListing
    queryset = ServerListing.objects.filter(status=1).order_by('-created_on')
    template_name = 'server-list.html'
    paginate_by = 10
