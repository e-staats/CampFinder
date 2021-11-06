"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importDefault(require("react"));
var Node = /** @class */ (function (_super) {
    __extends(Node, _super);
    function Node() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChange = function (e) {
            var regionName = _this.props.item.region;
            return _this.props.handleChange(e, regionName);
        };
        return _this;
    }
    Node.prototype.render = function () {
        var opacity = this.props.item.isChecked ? "100%" : "";
        var style = {
            transform: "translate(" + this.props.item.xPos.toString() + "px," + this.props.item.yPos.toString() + "px)",
            opacity: opacity
        };
        var cssClass = "map-circle-checkbox " + this.props.item.cssClass;
        if (typeof (this.props.handleChange) === 'undefined') {
            return (react_1["default"].createElement("div", { className: "origin-node", style: style },
                react_1["default"].createElement("span", null, this.props.item.name)));
        }
        return (react_1["default"].createElement("div", null,
            react_1["default"].createElement("label", { className: cssClass, style: style },
                react_1["default"].createElement("input", { key: this.props.item.id, type: "checkbox", name: this.props.item.name, value: this.props.item.name, checked: this.props.item.isChecked, onChange: this.handleChange }),
                react_1["default"].createElement("span", null, this.props.item.name))));
    };
    return Node;
}(react_1["default"].Component));
exports["default"] = Node;
