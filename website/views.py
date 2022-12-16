
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView

from website.models import ServerListing, Tag


class ServerListings(ListView):
    model = ServerListing
    queryset = ServerListing.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 10
