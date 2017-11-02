/**
 * Created by songchuanzhou on 17/1/5.
 */
alert("hello world in TypeScript");
function Add(left, right) {
    return left + right;
}
function area(shape) {
    var area = shape.width * shape.height;
    return "I'm a " + shape.name + " with an area of " + area + "cm squared.";
}
console.log(area({ name: "rectangle", width: 30, height: 15 }));
console.log(area({ name: "square", width: 40, height: 50 }));
