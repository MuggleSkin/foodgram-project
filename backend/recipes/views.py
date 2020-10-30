from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Recipe


def index(request):
    recipe_list = (
        Recipe.objects.select_related("author")
        .order_by("-pub_date")
        .all()
    )
    paginator = Paginator(recipe_list, 9)

    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    if request.user.is_authenticated:
        template_name = "indexAuth.html"
    else:
        template_name = "indexNotAuth.html"
    return render(
        request, template_name, {"page": page, "paginator": paginator}
    )
