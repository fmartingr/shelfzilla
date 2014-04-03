from django import template


register = template.Library()


@register.filter
def pjax(template_name, request, string="-pjax"):
    if isinstance(request, (bool, int)):
        is_pjax = request
    else:
        is_pjax = request.META.get("HTTP_X_PJAX", False)

    if is_pjax:
        name, extension = template_name.split('.')
        template_name = '{}{}.{}'.format(
            name, string, extension
        )
    return template_name.strip()
