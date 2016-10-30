'use strict';

var hljs = require('highlight.js');
var React = require('react');
var ReactDOM = require('react-dom');

var Highlight = React.createClass({
  displayName: 'Highlight',

  getDefaultProps: function getDefaultProps() {
    return {
      innerHTML: false,
      className: null,
      element: null
    };
  },
  componentDidMount: function componentDidMount() {
    this.highlightCode();
  },
  componentDidUpdate: function componentDidUpdate() {
    this.highlightCode();
  },
  highlightCode: function highlightCode() {
    var domNode = ReactDOM.findDOMNode(this);
    var nodes = domNode.querySelectorAll('pre code');
    if (nodes.length > 0) {
      for (var i = 0; i < nodes.length; i = i + 1) {
        hljs.highlightBlock(nodes[i]);
      }
    }
  },
  render: function render() {
    var Element = this.props.element ? React.DOM[this.props.element] : null;

    if (this.props.innerHTML) {
      if (!Element) {
        Element = React.DOM.div;
      }
      return Element({
        dangerouslySetInnerHTML: { __html: this.props.children },
        className: this.props.className || null
      }, null);
    } else {
      if (Element) {
        return Element({
          className: this.props.className
        }, this.props.children);
      } else {
        return React.createElement(
          'pre',
          null,
          React.createElement(
            'code',
            { className: this.props.className },
            this.props.children
          )
        );
      }
    }
  }
});

module.exports = Highlight;