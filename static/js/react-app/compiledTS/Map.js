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
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __spreadArray = (this && this.__spreadArray) || function (to, from, pack) {
    if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
        if (ar || !(i in from)) {
            if (!ar) ar = Array.prototype.slice.call(from, 0, i);
            ar[i] = from[i];
        }
    }
    return to.concat(ar || Array.prototype.slice.call(from));
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importDefault(require("react"));
var MapBody_1 = __importDefault(require("./resources/MapBody"));
var Map = /** @class */ (function (_super) {
    __extends(Map, _super);
    function Map(props) {
        var _this = _super.call(this, props) || this;
        _this.updateNodeCheckedStatus = function (parks, prevParks) {
            //Because the data structures are pretty weird, this is a two parter: get
            //the list of parks to update, then go through and update the nodes
            var parksToUpdate = {};
            for (var region in parks) {
                if (region === 'allChecked') {
                    continue;
                }
                for (var _i = 0, _a = parks[region]['parkList']; _i < _a.length; _i++) {
                    var park = _a[_i];
                    for (var _b = 0, _c = prevParks[region]['parkList']; _b < _c.length; _b++) {
                        var prevPark = _c[_b];
                        if (park.isChecked !== prevPark.isChecked) {
                            parksToUpdate[park.id] = park.isChecked;
                        }
                    }
                }
            }
            if (Object.keys(parksToUpdate).length === 0) {
                return;
            }
            _this.setState(function (prevState) {
                var nodes = prevState.nodes;
                for (var _i = 0, nodes_1 = nodes; _i < nodes_1.length; _i++) {
                    var node = nodes_1[_i];
                    if (node.id in parksToUpdate) {
                        node.isChecked = parksToUpdate[node.id];
                    }
                }
                return { nodes: nodes };
            });
        };
        _this.updateOrigin = function (origin) {
            var dimensions = _this.defineDimensions();
            var boundaries = _this.defineBoundaries();
            var pixelRates = _this.definePixelRate(dimensions, boundaries);
            var coordinates = _this.calcParkPosition(origin, boundaries, pixelRates);
            _this.setState(function (prevState) {
                var originNode = __assign(__assign({}, prevState.originNode), { id: 0, name: origin.name, xPos: coordinates[0], yPos: coordinates[1] });
                return { originNode: originNode };
            });
        };
        _this.addNode = function (id, nodeName, cssClass, xPos, yPos) {
            _this.setState(function (prevState) {
                var nodeInfo = { id: id, name: nodeName, cssClass: cssClass, xPos: xPos, yPos: yPos };
                var nodes = prevState.nodes;
                nodes = __spreadArray(__spreadArray([], prevState.nodes, true), [nodeInfo], false);
                return { nodes: nodes };
            });
        };
        _this.defineBoundaries = function () {
            return {
                north: 47.0,
                south: 42.15,
                east: -86.0,
                west: -93.0
            };
        };
        _this.definePixelRate = function (dimensions, boundaries) {
            var ewSpan = boundaries.west - boundaries.east;
            var nsSpan = boundaries.north - boundaries.south;
            var longPixelRate = dimensions[0] / ewSpan;
            var latPixelRate = dimensions[1] / nsSpan;
            return { lat: latPixelRate, long: longPixelRate };
        };
        _this.createNodesForParks = function (inputData) {
            var nodes = [];
            var dimensions = _this.defineDimensions();
            var boundaries = _this.defineBoundaries();
            var pixelRates = _this.definePixelRate(dimensions, boundaries);
            //
            //go find loop that gets parks out of my dumb data structure
            for (var region in inputData) {
                if (region === 'allChecked') {
                    continue;
                }
                for (var _i = 0, _a = inputData[region]['parkList']; _i < _a.length; _i++) {
                    var park = _a[_i];
                    var coordinates = _this.calcParkPosition(park, boundaries, pixelRates);
                    var node = {
                        id: park.id,
                        name: park.name,
                        cssClass: _this.getRegionClass(region),
                        xPos: coordinates[0],
                        yPos: coordinates[1],
                        region: region,
                        isChecked: park.isChecked
                    };
                    nodes.push(node);
                }
            }
            return nodes;
        };
        _this.calcParkPosition = function (park, boundaries, pixelRate) {
            var xPos = boundaries.west - park.lng;
            var yPos = boundaries.north - park.lat;
            return [xPos * pixelRate.long, yPos * pixelRate.lat];
        };
        _this.defineDimensions = function () {
            var width = document.getElementById('svg-map').clientWidth;
            return [width, width];
        };
        _this.getRegionClass = function (regionName) {
            var suffix = "-node";
            var cssClass = regionName + suffix;
            if (cssClass === null) {
                cssClass = 'default' + suffix;
            }
            return cssClass;
        };
        _this.handleChange = function (e, regionName) {
            var name = e.target.name;
            var checked = e.target.checked;
            _this.setState(function (prevState) {
                var nodes = prevState.nodes;
                nodes = nodes.map(function (item) { return item.name === name ? __assign(__assign({}, item), { isChecked: checked }) : item; });
                return { nodes: nodes };
            });
            _this.props.handleChange(e, regionName);
        };
        _this.state = {
            nodes: [],
            zipCode: "",
            originNode: {
                id: 0,
                name: 'undefined',
                cssClass: 'origin-node',
                xPos: 0,
                yPos: 0
            }
        };
        return _this;
    }
    Map.prototype.componentDidMount = function () {
        var _this = this;
        this.setState(function () {
            var nodes = _this.createNodesForParks(_this.props.parks);
            return { nodes: nodes };
        });
    };
    Map.prototype.componentDidUpdate = function (prevProps) {
        if (this.props.parks !== prevProps.parks) {
            this.updateNodeCheckedStatus(this.props.parks, prevProps.parks);
        }
        if (this.props.origin !== prevProps.origin) {
            this.updateOrigin(this.props.origin);
        }
    };
    Map.prototype.render = function () {
        return (react_1["default"].createElement("div", null,
            react_1["default"].createElement(MapBody_1["default"], { nodes: this.state.nodes, origin: this.state.originNode, handleChange: this.handleChange })));
    };
    return Map;
}(react_1["default"].Component));
exports["default"] = Map;
