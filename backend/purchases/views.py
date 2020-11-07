from io import StringIO
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .purchases import Purchases
from recipes.models import Recipe


def purchase(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    purchases = Purchases(request)

    if request.method == "POST":
        return JsonResponse({"success": purchases.add(recipe)})
    elif request.method == "DELETE":
        return JsonResponse({"success": purchases.remove(recipe)})


def purchase_list(request):
    purchases = Purchases(request)
    recipe_list = (
        Recipe.objects.select_related("author")
        .filter(id__in=purchases.get_ids()).all()
    )

    return render(request, "purchases.html", {"recipes": recipe_list,})

def get_shopping_list(request):
    purchases = Purchases(request)
    recipe_list = Recipe.objects.filter(id__in=purchases.get_ids()).all()
    used_ingredients = []
    for recipe in recipe_list:
        for ing in recipe.ingredients.all():
            is_unique = True
            for used in used_ingredients:
                if ing.data == used.data:
                    used.amount += ing.amount
                    is_unique = False
            if is_unique: used_ingredients.append(ing)

    shopping_list = StringIO()
    for ingredient in used_ingredients:
        shopping_list.write("•  " + str(ingredient) + "\n")

    response = HttpResponse(shopping_list.getvalue(), content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename="shopping.txt"'

    return response

def clear_purchases(request):
    purchases = Purchases(request)
    purchases.clear()
    return redirect("index")
