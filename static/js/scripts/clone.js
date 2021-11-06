//For use in cloning objects for updating state. How is this not in the standard library??
function clone(target, source) {

    for (let key in source) {

        // Use getOwnPropertyDescriptor instead of source[key] to prevent from trigering setter/getter.
        let descriptor = Object.getOwnPropertyDescriptor(source, key);
        if (descriptor.value instanceof String) {
            target[key] = new String(descriptor.value);
        }
        else if (descriptor.value instanceof Array) {
            target[key] = clone([], descriptor.value);
        }
        else if (descriptor.value instanceof Object) {
            let prototype = Reflect.getPrototypeOf(descriptor.value);
            let cloneObject = clone({}, descriptor.value);
            Reflect.setPrototypeOf(cloneObject, prototype);
            target[key] = cloneObject;
        }
        else {
            Object.defineProperty(target, key, descriptor);
        }
    }
    let prototype = Reflect.getPrototypeOf(source);
    Reflect.setPrototypeOf(target, prototype);
    return target;
}

export default clone