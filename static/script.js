/* Put your javascript here */
/* JQuery and AlpineJS are supported. */
$(function() {
  window.App = {};
  window.App.createEditor = function(container, initialJson) {
    const options = {
      mode: 'code',
      navigationBar: false,
      statusBar: false,
      mainMenuBar: false,
    }
    const editor = new JSONEditor(container, options)
    const value = $(container).data("value");
    if (value) {
      initialJson = value;
    }
    // set json
    editor.set(initialJson)

    // get json
    return editor;
  }

  window.App.initializeForm = function(container) {
    var handler = {};
    handler.el = container;
    container.find(".editor").each(function() {
      var name = $(this).data('name');
      handler[name] = window.App.createEditor(this, {});
    })
    return handler;
  }

  window.App.getPayload = function(handler) {
    var headersJSON = handler.headersEditor.get();
    var bodyJSON = handler.bodyEditor.get();
    var statusCode = parseInt(handler.el.find("[name='status_code']").val(), 10);
    var path = handler.el.find("[name='path']").val();
    var routeUuid = handler.el.find("[name='route_uuid']").val();
    var namespaceUuid = handler.el.find("[name='namespace_uuid']").val();
    var verb = handler.el.find("[name='verb']").val();

    var payload = {
      uuid: namespaceUuid,
      route: {
        uuid: routeUuid,
        namespace_uuid: namespaceUuid,
        path: path,
        status_code: statusCode,
        verb: verb,
        headers: headersJSON,
        body: bodyJSON,
      }
    };

    return payload;
  };
});
