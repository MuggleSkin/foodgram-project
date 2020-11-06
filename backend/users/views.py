from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.views.generic import CreateView
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CreationForm
from .models import Recipe
from django.core.paginator import Paginator


User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    success_url = "/auth/login/"
    template_name = "signup.html"


@login_required
def favorites(request):
    recipe_list = (
        request.user.social.favorites
        .select_related("author").order_by("-pub_date").all()
    )
    tag_names = request.GET.getlist("query")
    if tag_names:
        recipe_list = recipe_list.filter(tags__name__in=tag_names).distinct()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request, "favorites.html", {"page": page, "paginator": paginator}
    )


@login_required
def subscriptions(request):
    RECIPES_DISPLAYED = 3
    authors = request.user.social.following.all()
    authors_data = []
    for author in authors:
        data = dict()
        data["info"] = author
        data["recipes"] = author.recipes.order_by("-pub_date")[:RECIPES_DISPLAYED]
        data["recipes_left"] = author.recipes.count() - RECIPES_DISPLAYED
        authors_data.append(data)

    paginator = Paginator(authors_data, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request, "myFollow.html", {"page": page, "paginator": paginator}
    )


@login_required
def favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == "POST":
        request.user.social.favorites.add(recipe)
        return JsonResponse({"success": True})
    elif request.method == "DELETE":
        request.user.social.favorites.remove(recipe)
        return JsonResponse({"success": True})


@login_required
def subscribe(request, author_id):
    author = get_object_or_404(User, id=author_id)
    if request.user == author:
        return HttpResponseForbidden("You can't subscribe to yourself")

    if request.method == "POST":
        request.user.social.following.add(author)
        return JsonResponse({"success": True})
    elif request.method == "DELETE":
        request.user.social.following.remove(author)
        return JsonResponse({"success": True})
