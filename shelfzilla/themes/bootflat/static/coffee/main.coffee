if USE_PJAX
    NProgress.start()

    window._updateMessages = false
    window.updateMessagesHTML = ->
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

    window.imageLoad = (element) ->
        imgLoad = imagesLoaded(element)

        imgLoad.on 'done', (event) ->
            NProgress.done()

        imgLoad.on 'progress', (instance, image) ->
            inc = instance.images.length/1000
            NProgress.inc(inc)

    # Document ready
    $ ->
        # Update messages
        window.updateMessages()

        # Document load progress bar
        window.imageLoad(document)

        # Background
        #$.vegas
        #    src: '/static/backgrounds/shelves.jpg'
        #    fade: 1200
        #    #complete: -> NProgress.done()

        # PJAX
        if $.support.pjax
            $(document).on 'click', 'a[data-pjax]', (event) ->
                elem = $(@)
                pjax = elem.data('pjax')
                push = true

                nav_element = elem.closest('[data-pjax-nav]')

                nav_element.siblings('.active').removeClass('active')
                nav_element.addClass('active')

                if elem.is('[data-pjax-unnav]')
                    $('[data-pjax-nav].active').removeClass('active')

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
                    timeout: 5000,
                    push: push,
                    scrollTo: false
                }

                if elem.is('[pjax-messages]')
                    window._updateMessages = true

    # Nprogress
    $(document).on 'pjax:start', -> NProgress.start()
    $(document).on 'pjax:end', (event) ->
        window.imageLoad(event.target)

        if ga?
            ga('send', 'pageview')

        if window._updateMessages
            window.updateMessages()

# Tooltips
$('[data-toggle="tooltip"]').tooltip();
