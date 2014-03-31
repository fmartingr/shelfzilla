def pjax(request):
    """
    Determines if a request if a pjax request by the X-PJAX header
    """
    template = '_layout.html'
    is_pjax = request.META.get('HTTP_X_PJAX', False)

    if is_pjax:
        template = '_pjax.html'

    return {
        'is_pjax': is_pjax,
        'extends_template': template,
    }
