from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404, redirect, render

from .models import Recipe, User, Ingredient, IngredientForRecipe
from .forms import RecipeForm


def index(request):
    recipe_list = (
        Recipe.objects.select_related("author")
        .order_by("-pub_date")
        .all()
    )
    paginator = Paginator(recipe_list, 6)

    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    if request.user.is_authenticated:
        template_name = "indexAuth.html"
    else:
        template_name = "indexNotAuth.html"
    return render(
        request, template_name, {"page": page, "paginator": paginator}
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipe_list = (
        Recipe.objects.select_related("author")
        .filter(author=author)
        .order_by("-pub_date")
        .all()
    )
    paginator = Paginator(recipe_list, 6)

    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request, "authorRecipe.html", {
            "author": author,
            "page": page, 
            "paginator": paginator,
        },
    )


def recipe_view(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, author=author, id=recipe_id)

    if request.user.is_authenticated:
        template_name = "singlePage.html"
    else:
        template_name = "singlePageNotAuth.html"

    return render(
        request, template_name, {
            "author": author,
            "recipe": recipe,
        },
    )


def formify(post_data):
    post_data._mutable = True
    tags = ""
    for key in list(post_data):
        if key.startswith("nameIngredient"):
            pos = key.split("_")[1]
            title = post_data.pop(key)[0]
            amount = float(post_data.pop(f"valueIngredient_{pos}")[0])
            dimension = post_data.pop(f"unitsIngredient_{pos}")[0]
            ingredient = get_object_or_404(
                Ingredient, 
                title=title, 
                dimension=dimension
            )
            instance = IngredientForRecipe.objects.get_or_create(
                ingredient=ingredient,
                amount=amount
            )[0]
            post_data.appendlist("ingredients", str(instance.id))
        elif key in ("breakfast", "dinner", "lunch"):
            if post_data.pop(key)[0] == "on":
                tags += key + " "
    post_data["tags"] = tags.rstrip()
    post_data._mutable = False
    return post_data


@login_required
def new_recipe(request):
    data = formify(request.POST) if request.POST else None
    form = RecipeForm(data, files=request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            unsaved_recipe = form.save(commit=False)
            unsaved_recipe.author = request.user
            unsaved_recipe.save()
            form.save_m2m()
            return redirect("index")

    return render(request, "formRecipe.html", {"form": form})


@login_required
def recipe_edit(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        return redirect("recipe", username=username, recipe_id=recipe_id)
    recipe = get_object_or_404(Recipe, author=author, id=recipe_id)

    data = formify(request.POST) if request.POST else None
    form = RecipeForm(data, files=request.FILES or None, instance=recipe)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("recipe", username=username, recipe_id=recipe_id)

    return render(request, "formChangeRecipe.html", {
        "form": form,
        "recipe": recipe
    })


@login_required
def subscriptions(request):
    authors = request.user.social.following.all()
    authors_data = []
    for author in authors:
        data = dict()
        data["info"] = author
        data["recipes"] = author.recipes.order_by("-pub_date")[:3]
        data["recipes_left"] = author.recipes.count() - 3
        authors_data.append(data)

    paginator = Paginator(authors_data, 6)

    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request, "myFollow.html", {"page": page, "paginator": paginator}
    )


@login_required
def favorites(request):
    recipe_list = (
        request.user.social.favorites
        .select_related("author").order_by("-pub_date").all()
    )
    paginator = Paginator(recipe_list, 6)

    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request, "favorites.html", {"page": page, "paginator": paginator}
    )


def ingredients(request):
    result = Ingredient.objects.all()
    query = request.GET.get("query")
    if query: result = result.filter(title__istartswith=query)
    raw_data = serialize("python", result)
    formatted_data = [item['fields'] for item in raw_data]
    return JsonResponse(formatted_data, safe=False)
