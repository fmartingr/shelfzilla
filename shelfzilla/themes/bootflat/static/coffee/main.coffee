NProgress.start()

window._updateMessages = false
window.updateMessagesHtml = ->
    $.pjax
        url: '/messages/'
        container: '[data-pjax-container="messages"]'
        push: false
    window._updateMessages = false

window.updateMessages = ->
    $.getJSON "/messages/?format=json", (data) ->
        for message in data
            toastr[message.extra_tags](message.message)
    window._updateMessages = false

# Document ready
$ ->
    NProgress.inc(0.3)
    # Background
    $.vegas
        src: '/static/backgrounds/shelves.jpg'
        fade: 1200
        complete: -> NProgress.done()

    # PJAX
    if $.support.pjax
        $(document).on 'click', 'a[data-pjax]', (event) ->
            elem = $(@)
            pjax = elem.data('pjax')
            push = true
            if elem.is('[pjax-nopush]')
                push = false
            if not pjax
                container = $('[data-pjax-container="main"]')
            else if pjax == 'closest'
                container = elem.closest('[data-pjax-container]')
            else
                container = $("[data-pjax-container='#{pjax}']")

            $.pjax.click event, {
                container: container,
                timeout: 1000,
                push: push
            }

            if elem.is('[pjax-messages]')
                window._updateMessages = true

    # Update messages
    window.updateMessages()

# Tooltips
$('[data-toggle="tooltip"]').tooltip();

# Nprogress
$(document).on 'pjax:start', -> NProgress.start()
$(document).on 'pjax:end', ->
    NProgress.done()
    if window._updateMessages
        window.updateMessages()
