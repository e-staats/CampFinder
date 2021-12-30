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
var Button_1 = __importDefault(require("./resources/Button"));
var MapBody_1 = __importDefault(require("./resources/MapBody"));
var Map = /** @class */ (function (_super) {
    __extends(Map, _super);
    function Map(props) {
        var _this = _super.call(this, props) || this;
        _this.updateCheckedStatus = function (parks, prevParks) {
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
        _this.getDistanceData = function (origin) {
            return _this.hardcodedTestData(); //
        };
        _this.submitOnClick = function () {
            var origin = _this.state.zipCode;
            if (_this.validateZipCode(origin) === false) {
                console.log("add the fail case here " + origin);
                return;
            }
            var distanceData = _this.getDistanceData(origin);
            _this.setState(function (prevState) {
                var parks = distanceData.parks;
                var nodes = prevState.nodes;
                var originData = distanceData.origin;
                var origin = _this.calcOriginPosition(originData);
                return { nodes: nodes, origin: origin };
            });
        };
        _this.addNode = function (id, nodeName, color, xPos, yPos) {
            _this.setState(function (prevState) {
                var nodeInfo = { id: id, name: nodeName, color: color, xPos: xPos, yPos: yPos };
                var nodes = prevState.nodes;
                nodes = __spreadArray(__spreadArray([], prevState.nodes, true), [nodeInfo], false);
                return { nodes: nodes };
            });
        };
        _this.handleTextInput = function (event) {
            _this.setState({ zipCode: event.target.value });
        };
        _this.validateZipCode = function (zipCode) {
            if (typeof (Number(zipCode)) !== "number") {
                return false;
            }
            if (zipCode.length !== 5) {
                return false;
            }
            return true;
        };
        _this.defineBoundaries = function () {
            return {
                north: 47.1,
                south: 42.3,
                east: -86.4,
                west: -93.2
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
                        color: _this.getRegionColor(region),
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
        _this.calcOriginPosition = function (origin) {
            var dimensions = _this.defineDimensions();
            var boundaries = _this.defineBoundaries();
            var pixelRates = _this.definePixelRate(dimensions, boundaries);
            var coordinates = _this.calcParkPosition(origin, boundaries, pixelRates);
            return {
                id: '0',
                name: origin.name,
                xPos: coordinates[0],
                yPos: coordinates[1],
                color: 'FFFFFF'
            };
        };
        _this.defineDimensions = function () {
            return [1000, 1000];
        };
        _this.getRegionColor = function (regionName) {
            var color = "FFFFFF";
            switch (regionName) {
                case ("northwest"):
                    color = "#fad87b";
                    break;
                case ("northeast"):
                    color = "#b1d5bc";
                    break;
                case ("southwest"):
                    color = "#bcd682";
                    break;
                case ("southeast"):
                    color = "#ffca6e";
                    break;
                default:
                    color = "#FFFFFF";
            }
            return color;
        };
        _this._handleKeyDown = function (e) {
            if (e.key === 'Enter') {
                _this.submitOnClick();
            }
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
        _this.hardcodedTestData = function () {
            return {
                'origin': {
                    'id': 0,
                    'isChecked': false,
                    'name': '53703',
                    'lat': 43.07,
                    'lng': -89.37
                },
                'parks': {
                    '1': {
                        'distance': '312 mi',
                        'time': '4 hours 43 mins'
                    },
                    '24': {
                        'distance': '28.0 mi',
                        'time': '34 mins'
                    },
                    '3': {
                        'distance': '332 mi',
                        'time': '6 hours 24 mins'
                    },
                    '4': {
                        'distance': '76.2 mi',
                        'time': '1 hour 31 mins'
                    },
                    '43': {
                        'distance': '126 mi',
                        'time': '2 hours 1 min'
                    },
                    '42': {
                        'distance': '31.6 mi',
                        'time': '36 mins'
                    },
                    '7': {
                        'distance': '317 mi',
                        'time': '4 hours 54 mins'
                    },
                    '37': {
                        'distance': '199 mi',
                        'time': '3 hours 17 mins'
                    },
                    '46': {
                        'distance': '84.8 mi',
                        'time': '1 hour 28 mins'
                    },
                    '10': {
                        'distance': '52.0 mi',
                        'time': '1 hour 3 mins'
                    }
                }
            };
        };
        _this.state = {
            nodes: [],
            zipCode: "",
            origin: {
                id: '0',
                name: 'undefined',
                xPos: 0,
                yPos: 0,
                color: 'FFFFFF'
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
            this.updateCheckedStatus(this.props.parks, prevProps.parks);
        }
    };
    Map.prototype.render = function () {
        return (react_1["default"].createElement("div", null,
            react_1["default"].createElement("label", null, "Starting Zip Code:"),
            react_1["default"].createElement("input", { type: "text", id: "zipCode", placeholder: "Zip Code", onChange: this.handleTextInput, onKeyDown: this._handleKeyDown }),
            react_1["default"].createElement(Button_1["default"], { text: "Submit ZIP", onClick: this.submitOnClick }),
            react_1["default"].createElement(MapBody_1["default"], { nodes: this.state.nodes, origin: this.state.origin, handleChange: this.handleChange })));
    };
    return Map;
}(react_1["default"].Component));
exports["default"] = Map;
