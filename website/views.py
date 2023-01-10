
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View, generic
from django.views.generic.list import ListView
from django.urls import reverse_lazy



from .models import ServerListing, Game
from .forms import ProfileForm, CreateServerListingForm



def index(request):
    games = Game.objects.filter(status=1)
    for x in games:
        print(x.image)
    ctx = {'games': games}
    return render(request, "index.html", ctx)


def login(request):
    return render(request, "registration/login.html")


@login_required
def server_create(request):

    if request.method == 'POST':

        form = CreateServerListingForm(request.POST)

        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            return redirect('my-account')

    else:
        pass

    return render(
        request,
        "server_create.html",
        {
            'form': CreateServerListingForm(),
        }
    )


@login_required
def myaccount(request):
    if request.method == 'POST':

        form = ProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='my-account')
    else:
        username = request.user
        queryset = ServerListing.objects.filter(owner=username).order_by('-created_on')
        num_of_listings = queryset.count()
        form = ProfileForm(instance=request.user)

    return render(
        request,
        'registration/my_account.html',
        {
            'form': form,
            "serverlisting": queryset,
            'num_of_listings' : num_of_listings,
        }
    )


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


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