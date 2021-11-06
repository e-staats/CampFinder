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
var Node_1 = __importDefault(require("./Node"));
var MapBody = /** @class */ (function (_super) {
    __extends(MapBody, _super);
    function MapBody() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChange = function (e, regionName) {
            return _this.props.handleChange(e, regionName);
        };
        return _this;
    }
    MapBody.prototype.render = function () {
        var _this = this;
        var origin;
        if (this.props.origin.name !== 'undefined') {
            origin = react_1["default"].createElement(Node_1["default"], { item: this.props.origin });
        }
        else {
            origin = react_1["default"].createElement("div", null);
        }
        return (react_1["default"].createElement("div", null,
            react_1["default"].createElement("div", { className: "container" },
                origin,
                this.props.nodes.map(function (info, index) { return (react_1["default"].createElement(Node_1["default"], { item: info, handleChange: _this.handleChange })); }))));
    };
    return MapBody;
}(react_1["default"].Component));
exports["default"] = MapBody;
