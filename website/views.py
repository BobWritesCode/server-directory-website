
from django.shortcuts import render, get_object_or_404
from django.views import View
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

    def get(self, request, slug, *args, **kwargs):
        game = get_object_or_404(Game, slug=slug)
        queryset = ServerListing.objects.filter(status=1, game=game).order_by('-created_on')

        return render(
            request,
            "server-list.html",
            {
                "serverlisting": queryset,
            },
        )


class ServerDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = ServerListing.objects.filter(status=1)
        server = get_object_or_404(queryset, slug=slug)

        return render(
            request,
            "server_detail.html",
            {
                "server": server,
            },
        )