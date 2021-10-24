"use strict";
exports.__esModule = true;
//For use in cloning objects for updating state. How is this not in the standard library??
function clone(target, source) {
    for (var key in source) {
        // Use getOwnPropertyDescriptor instead of source[key] to prevent from trigering setter/getter.
        var descriptor = Object.getOwnPropertyDescriptor(source, key);
        if (descriptor.value instanceof String) {
            target[key] = new String(descriptor.value);
        }
        else if (descriptor.value instanceof Array) {
            target[key] = clone([], descriptor.value);
        }
        else if (descriptor.value instanceof Object) {
            var prototype_1 = Reflect.getPrototypeOf(descriptor.value);
            var cloneObject = clone({}, descriptor.value);
            Reflect.setPrototypeOf(cloneObject, prototype_1);
            target[key] = cloneObject;
        }
        else {
            Object.defineProperty(target, key, descriptor);
        }
    }
    var prototype = Reflect.getPrototypeOf(source);
    Reflect.setPrototypeOf(target, prototype);
    return target;
}
exports["default"] = clone;
