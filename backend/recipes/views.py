from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404, redirect, render

from .models import Recipe, User, Ingredient, RecipeIngredient
from .forms import RecipeForm


def index(request):
    recipe_list = (
        Recipe.objects.select_related("author")
        .order_by("-pub_date")
        .all()
    )
    tag_names = request.GET.getlist("query")
    if tag_names:
        recipe_list = recipe_list.filter(tags__name__in=tag_names).distinct()

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
    tag_names = request.GET.getlist("query")
    if tag_names:
        recipe_list = recipe_list.filter(tags__name__in=tag_names).distinct()

    paginator = Paginator(recipe_list, 6)

    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request, "profile.html", {
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


def formify(query_dict):
    data = query_dict.copy()
    tags = ""
    for key in list(data):
        if key.startswith("nameIngredient"):
            pos = key.split("_")[1]
            title = data.pop(key)[0]
            dimension = data.pop(f"unitsIngredient_{pos}")[0]
            amount = int(data.pop(f"valueIngredient_{pos}")[0])
            data.appendlist("ingredients", [title, dimension, amount])
        elif key in ("breakfast", "dinner", "lunch"):
            if data.pop(key)[0] == "on":
                tags += key + " "
    data["tags"] = tags.rstrip()
    return data


@login_required
def new_recipe(request):
    data = formify(request.POST) if request.POST else None
    form = RecipeForm(data, files=request.FILES or None)
  
    if request.method == "POST":
        if "ingredients" not in data:
            form.add_error(None, "Добавьте ингредиенты")
        if form.is_valid():
            unsaved_recipe = form.save(commit=False)
            unsaved_recipe.author = request.user
            unsaved_recipe.save()
            form.save_m2m()
            for title, dimension, amount in data.getlist("ingredients"):
                ingredient_data = get_object_or_404(
                    Ingredient,
                    title=title,
                    dimension=dimension
                )
                RecipeIngredient.objects.get_or_create(
                    data=ingredient_data,
                    recipe=unsaved_recipe,
                    amount=amount
                )
                unsaved_recipe.ingredients_data.add(ingredient_data)
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
        if "ingredients" not in data:
            form.add_error(None, "Добавьте ингредиенты")
        if form.is_valid():
            recipe = form.instance
            initial = recipe.ingredients_data.all()
            for title, dimension, amount in data.getlist("ingredients"):
                ingredient_data = get_object_or_404(
                    Ingredient,
                    title=title,
                    dimension=dimension
                )
                RecipeIngredient.objects.get_or_create(
                    data=ingredient_data,
                    recipe=recipe,
                    amount=amount
                )
                recipe.ingredients_data.add(ingredient_data)
                if ingredient_data in initial:
                    initial = initial.exclude(id=ingredient_data.id)
            for ing in initial:
                recipe.ingredients_data.remove(ing)
            form.save()
            return redirect("recipe", username=username, recipe_id=recipe_id)

    return render(request, "formChangeRecipe.html", {
        "form": form,
        "recipe": recipe
    })


@login_required
def recipe_delete(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        return redirect("recipe", username=username, recipe_id=recipe_id)
    recipe = get_object_or_404(Recipe, author=author, id=recipe_id)
    recipe.delete()
    return redirect("profile", username=username)


def ingredients(request):
    result = Ingredient.objects.all()
    query = request.GET.get("query", "").lower()
    if query:
        result = result.filter(title__startswith=query)
    raw_data = serialize("python", result)
    formatted_data = [item['fields'] for item in raw_data]
    return JsonResponse(formatted_data, safe=False)
