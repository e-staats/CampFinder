"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importDefault(require("react"));
function Button(_a) {
    var text = _a.text, onClick = _a.onClick;
    return (react_1["default"].createElement("button", { type: "button", className: "zipCodeButton", onClick: onClick }, text));
}
exports["default"] = Button;
