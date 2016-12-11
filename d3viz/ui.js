_.templateSettings = {
    evaluate:    /{{([\s\S]+?)}}/g,
    interpolate: /{{=([\s\S]+?)}}/g,
    escape:      /{{-([\s\S]+?)}}/g
};

var calloutTemplate = _.template($('#calloutContent').html());
var $callout = $('.callout');
var defaultNode = null;

var cleanNode = function cleanNode (dirty) {
  var attributes = _.clone(dirty);
  delete attributes.index;
  delete attributes.vx;
  delete attributes.vy;
  delete attributes.x;
  delete attributes.y;
  return attributes
}

var showCallout = instantShowCallout = function showCallout (dirty) {
  var attributes = cleanNode(dirty);

  $callout
    .html(calloutTemplate({
      id: attributes.id,
      attributes: attributes
    }))
    .show();
};

showCallout = _.debounce(showCallout, 300);

var setDefaultCallout = function setDefaultCallout(dirty) {
  defaultNode = cleanNode(dirty);
  instantShowCallout(dirty);
}


var hideCallout = function hideCallout () {
  $callout.hide();
  if (defaultNode !== null) {
    showCallout(defaultNode);
  }
}
