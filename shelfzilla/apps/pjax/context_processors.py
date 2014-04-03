def pjax(request):
    """
    Determines if a request if a pjax request by the X-PJAX header
    """
    is_pjax = request.META.get('HTTP_X_PJAX', False)

    return {
        'is_pjax': is_pjax,
    }
