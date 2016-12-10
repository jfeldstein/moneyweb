_.templateSettings = {
    evaluate:    /{{([\s\S]+?)}}/g,
    interpolate: /{{=([\s\S]+?)}}/g,
    escape:      /{{-([\s\S]+?)}}/g
};

var calloutTemplate = _.template($('#calloutContent').html());
var $callout = $('.callout');

var showCallout = function showCallout (dirty) {
  var attributes = _.clone(dirty);
  delete attributes.index;
  delete attributes.vx;
  delete attributes.vy;
  delete attributes.x;
  delete attributes.y;

  $callout
    .html(calloutTemplate({
      id: attributes.id,
      attributes: attributes
    }))
    .show();
}

var hideCallout = function hideCallout () {
  $callout.hide();
}
