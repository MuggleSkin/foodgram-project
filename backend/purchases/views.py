from io import StringIO
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Purchase, Session, Recipe


def purchase(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    request.session.save()
    session = Session.objects.get(pk=request.session.session_key)
    purchase = Purchase.objects.get_or_create(session=session)[0]

    if request.method == "POST":
        purchase.recipes.add(recipe)
        return JsonResponse({"success": True})
    elif request.method == "DELETE":
        purchase.recipes.remove(recipe)
        return JsonResponse({"success": True})


def purchase_list(request):
    return render(request, "purchases.html")


def get_shopping_list(request):
    session = Session.objects.get(pk=request.session.session_key)
    purchase = Purchase.objects.get_or_create(session=session)[0]
    used_ingredients = []

    for recipe in purchase.recipes.all():
        for ing in recipe.ingredients.all():
            is_unique = True
            for used in used_ingredients:
                if ing.data == used.data:
                    used.amount += ing.amount
                    is_unique = False
            if is_unique: 
                used_ingredients.append(ing)

    shopping_list = StringIO()
    for ingredient in used_ingredients:
        shopping_list.write("•  " + str(ingredient) + "\n")

    response = HttpResponse(
        shopping_list.getvalue(),
        content_type="text/plain"
    )
    response['Content-Disposition'] = 'attachment; filename="shopping.txt"'

    return response


def purchase_clear(request):
    session = Session.objects.get(pk=request.session.session_key)
    purchase = Purchase.objects.get_or_create(session=session)[0]
    purchase.recipes.clear()
    return redirect("index")
