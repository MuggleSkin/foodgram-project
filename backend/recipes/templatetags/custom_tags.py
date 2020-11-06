from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def add_get_param(context, key, val):
    """
    Generate and return current page's url with get param key=val
    Doesn't change actual request.GET dict
    """
    request = context["request"]
    params = request.GET.copy()
    if key in params and val in params.getlist(key) :
        return request.get_full_path()
    params.appendlist(key, val)
    
    # Reset paginator in case get param impacts filtering
    if key == "query" and "page" in params:
        del params["page"]

    query_path = params.urlencode()
    if query_path: query_path = "?" + query_path
    return request.path + query_path

@register.simple_tag(takes_context=True)
def remove_get_param(context, key, val):
    """
    Generate and return current page's url with removed get param key=val
    Doesn't change actual request.GET dict
    """
    request = context["request"]
    params = request.GET.copy()
    values = params.getlist(key)
    if key not in params or val not in values:
        return request.get_full_path()

    if len(values) == 1:
        del params[key]
    else:
        values.remove(val)
        params.setlist(key, values)

    # Reset paginator in case get param impacts filtering
    if key == "query" and "page" in params:
        del params["page"]

    query_path = params.urlencode()
    if query_path: query_path = "?" + query_path
    return request.path + query_path

@register.simple_tag(takes_context=True)
def replace_get_param(context, key, new_val):
    """
    Generate and return current page's url with replaced get param key=new_val
    Doesn't change actual request.GET dict
    """
    request = context["request"]
    params = request.GET.copy()
    params[key] = new_val

    # Reset paginator in case get param impacts filtering
    if key == "query" and "page" in params:
        del params["page"]

    query_path = params.urlencode()
    if query_path: query_path = "?" + query_path
    return request.path + query_path
