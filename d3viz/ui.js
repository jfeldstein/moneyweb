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
  delete attributes.group;
  delete attributes.fx;
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


var toggleNodesAround = function toggleNodesAround(node) {
  var $node = $('.circle.'+idToClass(node.id));
  var centerClass = $node.attr('class').replace(/ ?circle ?/, '');
  var $lines = $('.line.source-'+centerClass);
  var isCenterHuman = false;

  if ($lines.length === 0) {
    $lines = $('.line.target-'+centerClass);

    if ($lines.length === 0) {
      return;
    }

    isCenterHuman = true;
  }

  var otherClasses = Array.from($lines.map(function(i, l) { return Array.from(l.classList); }));
  otherClasses = _.uniqBy(otherClasses)
  otherClasses = _.without(otherClasses, 'line', 'circle');
  var linesAndNodes = _.groupBy(otherClasses, function(cls) {
    return cls.indexOf('source') !== -1 ? 'lines' : 'circles';
  });

  if (isCenterHuman) {
    var destCircles = linesAndNodes['lines'];

    destCircles = destCircles.map(function(circle){
      return circle.replace('source-', '');
    })

    linesAndNodes['circles'] = destCircles;
    linesAndNodes['circles'].push(centerClass);
    linesAndNodes['lines'] = ['target-'+centerClass]
  }

  var circlesToKeep = linesAndNodes['circles'].map(function(circle) {return '.'+circle.replace('target-', ''); });
  circlesToKeep.push('.'+centerClass);
  circlesToKeep = circlesToKeep.join(', ');

  var linesToKeep = linesAndNodes['lines'].map(function(line) {return '.'+line; }).join(', ');
  var selector = ['.circle:not(',circlesToKeep,'), .line:not(',linesToKeep,')'].join(' ');

  $(selector).hide();
}

var clearFocus = function clearFocus() {
  $('.circle, .line').show();
};

var setFocus = function setFocus(dirty) {
  defaultNode = cleanNode(dirty);
  instantShowCallout(dirty);
  toggleNodesAround(dirty);
}


var hideCallout = function hideCallout () {
  $callout.hide();
  if (defaultNode !== null) {
    showCallout(defaultNode);
  }
}
