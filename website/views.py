
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View, generic
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from cloudinary import uploader
from .models import ServerListing, Game, Tag
from .forms import ProfileForm, CreateServerListingForm


def index(request):
    games = Game.objects.filter(status=1)
    ctx = {
        'games': games,
        'tag_string' : "0",
        }
    return render(request, "index.html", ctx)


@login_required
def server_create(request):
    if request.method == 'POST':
        form = CreateServerListingForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES:
                image = uploader.upload(request.FILES['logo'])
                form.instance.logo = image['url']
            form.instance.owner = request.user
            form.save()
            return redirect('my-account')
        else:
            return render(
                request,
                "server_create.html",
                {
                    'form': form,
                }
            )
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
def server_edit(request, item_pk):
    item = get_object_or_404(ServerListing, pk=item_pk)
    if request.method == "POST":
        form = CreateServerListingForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            if request.FILES:
                image = uploader.upload(request.FILES['logo'])
                form.instance.logo = image['url']
            form.save()
            return redirect('my-account')

    form = CreateServerListingForm(instance=item)

    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'server_edit.html', context)


@login_required
def server_delete(request, item_pk):
    item = get_object_or_404(ServerListing, pk=item_pk)
    item.delete()
    return redirect('my-account')


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


class LoginView(generic.CreateView):
    template_name = "registration/signup.html"
    authentication_form = AuthenticationForm
    success_url = reverse_lazy("home")


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def server_listings(request, slug, tag_string=""):
    game = get_object_or_404(Game, slug=slug)
    tags = game.tags.all()

    query = Q(status=1) & Q(game=game)
    queryset = ServerListing.objects.filter(query).distinct()

    all_tags_for_game = []
    for x in tags:
        all_tags_for_game.append([x.id, x.name])

    ' Manage tag_string'
    if tag_string != "":
        'Create list from string'
        selected_tags = tag_string.split("%")
        'Check to see if adding or removing tag'
        action = selected_tags.pop(0)

        'A = add tag, R = remove tag'
        if action == "A":
            'Prepare new tag_string to send to front-end'
            tag_string = '%' + '%'.join(selected_tags)

        else:
            'Which tag has been selected to be removed'
            to_be_removed = selected_tags.pop(0)

            'Remove tag from selected list'
            selected_tags.remove(to_be_removed)

            'Check to see if all tags have been unselected'
            'Prepare tag_string'
            if len(selected_tags) != 0:
                tag_string = '%' + '%'.join(selected_tags)
            else:
                tag_string = ''

        'Narrows server list down based on tags picked by user'
        for value in selected_tags:
            queryset = queryset.filter(tags__name=value)

        'Use list comprehension to remove selected tags from all available tags'
        tags = [x for x in game.tags.all() if x.name not in selected_tags]

    else:
        'If tag_string empty then create empty list'
        selected_tags = []
        'Get all available tags for game selected'
        tags = game.tags.all()

    return render(
        request,
        "server-list.html",
        {
            "serverlisting": queryset,
            "selected_tags": selected_tags,
            "tags": tags,
            "tag_string": tag_string,
            "slug": slug,
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