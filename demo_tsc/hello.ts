/**
 * Created by songchuanzhou on 17/1/5.
 */

alert("hello world in TypeScript");

function Add(left: number, right: number): number {
    return left + right;
}

function area(shape: string, width: number, height: number) {
    var area = width * height;
    return "I'm a " + shape + " with an area of " + area + "cm squared.";
}