from .models import Purchase, Session


def get_purchase(request):
    """
    Возвращает объект модели Purchase для текущей сессии
    """
    try:
        session = Session.objects.get(pk=request.session.session_key)
        purchase = Purchase.objects.get_or_create(session=session)[0]
    except Session.DoesNotExist:
        purchase = None
    return {"purchase": purchase}
