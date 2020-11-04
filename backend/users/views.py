from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.views.generic import CreateView
from django.shortcuts import get_object_or_404, redirect

from .models import Follow
from .forms import CreationForm


User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    success_url = "/auth/login/"
    template_name = "signup.html"


@login_required
def subscribe(request, author_id):
    author = get_object_or_404(User, id=author_id)

    if request.user == author:
        if request.is_ajax():
            return HttpResponseForbidden("You can't subscribe to yourself")
        return redirect("profile", username=author.username)

    Follow.objects.get_or_create(user=request.user, author=author)
    if request.is_ajax():
        return JsonResponse({"success": True})
    return redirect("profile", username=author.username)


@login_required
def unsubscribe(request, author_id):
    author = get_object_or_404(User, id=author_id)

    if request.user == author:
        if request.is_ajax():
            return HttpResponseForbidden("You can't subscribe to yourself")
        return redirect("profile", username=author.username)
        
    follow = get_object_or_404(Follow, user=request.user, author=author)
    follow.delete()
    if request.is_ajax():
        return JsonResponse({"success": True})
    return redirect("profile", username=author.username)
