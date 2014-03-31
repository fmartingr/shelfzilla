NProgress.start()

window.updateMessages = ->
    jQuery.pjax
        url: '/messages/'
        container: '[data-pjax-container="messages"]'
        push: false

jQuery ->
    NProgress.inc(0.3)
    # Background
    jQuery.vegas
        src: '/static/backgrounds/shelves.jpg'
        fade: 1200
        complete: -> NProgress.done()

    # PJAX
    if jQuery.support.pjax
        jQuery(document).on 'click', 'a[data-pjax]', (event) ->
            elem = jQuery(@)
            container = elem.data('container')
            if not container
                container = jQuery('[data-pjax-container="main"]')
            if container == 'closest'
                container = jQuery(@).closest('[data-pjax-container]')
            else
                container = jQuery(container)

            jQuery.pjax.click event, {
                container: container,
                timeout: 1000
            }

# Tooltips
jQuery('[data-toggle="tooltip"]').tooltip();

# Nprogress
jQuery(document).on 'pjax:start', -> NProgress.start()
jQuery(document).on 'pjax:end', -> NProgress.done()
