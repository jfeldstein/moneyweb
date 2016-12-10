_.templateSettings = {
    evaluate:    /{{([\s\S]+?)}}/g,
    interpolate: /{{=([\s\S]+?)}}/g,
    escape:      /{{-([\s\S]+?)}}/g
};

var calloutTemplate = _.template($('#calloutContent').html());
var $callout = $('.callout');

var showCallout = function showCallout (attributes) {
  $callout
    .html(calloutTemplate({
      name: attributes.name,
      attributes: attributes
    }))
    .show();
}

var hideCallout = function hideCallout () {
  $callout.hide();
}
