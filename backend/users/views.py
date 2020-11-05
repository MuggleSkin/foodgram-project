from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.views.generic import CreateView
from django.shortcuts import get_object_or_404, redirect

from .forms import CreationForm
from .models import Recipe


User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    success_url = "/auth/login/"
    template_name = "signup.html"


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


@login_required
def favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == "POST":
        request.user.social.favorites.add(recipe)
        return JsonResponse({"success": True})
    elif request.method == "DELETE":
        request.user.social.favorites.remove(recipe)
        return JsonResponse({"success": True})