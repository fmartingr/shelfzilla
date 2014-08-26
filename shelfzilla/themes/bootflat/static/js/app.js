toastr.options = {
  "positionClass": "toast-top-left"
};

window._updateMessages = false;

window.updateMessagesHTML = function() {
  $.pjax({
    url: '/messages/',
    container: '[data-pjax-container="messages"]',
    push: false
  });
  return window._updateMessages = false;
};

window.updateMessages = function() {
  $.getJSON("/messages/?format=json", function(data) {
    var message, _i, _len, _results;
    _results = [];
    for (_i = 0, _len = data.length; _i < _len; _i++) {
      message = data[_i];
      _results.push(toastr[message.extra_tags](message.message));
    }
    return _results;
  });
  return window._updateMessages = false;
};

var getContainerFor = function(elem) {
  pjax = elem.data('pjax');
  if (!pjax) {
    container = $('[data-pjax-container="main"]');
  } else if (pjax === 'closest') {
    container = elem.closest('[data-pjax-container]');
  } else {
    container = $("[data-pjax-container='" + pjax + "']");
  }
  return container;
}

if (USE_PJAX) {
  NProgress.start();
  window.imageLoad = function(element) {
    var imgLoad;
    imgLoad = imagesLoaded(element);
    imgLoad.on('done', function(event) {
      return NProgress.done();
    });
    return imgLoad.on('progress', function(instance, image) {
      var inc;
      inc = instance.images.length / 1000;
      return NProgress.inc(inc);
    });
  };
  $(function() {
    window.updateMessages();
    window.imageLoad(document);
    if ($.support.pjax) {
      $(document).on('click', 'a[data-pjax]', function(event) {
        var container, elem, nav_element, pjax, push;
        elem = $(this);
        container = getContainerFor(elem)
        push = true;
        nav_element = elem.closest('[data-pjax-nav]');
        nav_element.siblings('.active').removeClass('active');
        nav_element.addClass('active');
        if (elem.is('[data-pjax-unnav]')) {
          $('[data-pjax-nav].active').removeClass('active');
        }
        if (elem.is('[pjax-nopush]')) {
          push = false;
        }

        $.pjax.click(event, {
          container: container,
          timeout: 5000,
          push: push,
          scrollTo: false
        });
        if (elem.is('[pjax-messages]')) {
          return window._updateMessages = true;
        }
      });
      $(document).on('submit', 'form[data-pjax]', function(event) {
        container = getContainerFor($(this));
        $.pjax.submit(event, container)
      })
    }
  });
  $(document).on('pjax:start', function() {
    return NProgress.start();
  });
  $(document).on('pjax:end', function(event) {
    window.imageLoad(event.target);
    if (typeof ga !== "undefined" && ga !== null) {
      ga('send', 'pageview');
    }
    if (window._updateMessages) {
      return window.updateMessages();
    }
  });
}

$('[data-toggle="tooltip"]').tooltip();
