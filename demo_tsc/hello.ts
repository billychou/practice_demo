/**
 * Created by songchuanzhou on 17/1/5.
 */

alert("hello world in TypeScript");

function Add(left: number, right: number): number {
    return left + right;
}


//接口类型批注
interface Shape {
    name: string;
    width: number;
    height: number;
    color?: string;
}

function area(shape: Shape) {
    var area = shape.width * shape.height;
    return "I'm a " + shape.name + " with an area of " + area + "cm squared.";
}

//function 更换成 ()=>
var shape1 = {
    name: "rectangle",
    popup: function(){
        console.log('This inside popup():', this.name);
        setTimeout(function(){
            console.log("This inside setTimeout():", this.name);
            console.log("I'm a " + this.name + "!");
        }, 3000);
    }
};



class Shape2 {
    area: number;
    color: string;
    constructor (name: string, width: number, height: number) {
        this.area = width * height;
        this.color = "pink";
    };

    shoutout() {
        return "I'm " + this.color + " " + this.name + " with an area of " + this.area + "cm squared.";
    }
}

console.log( area({name: "rectangle", width: 30, height: 15}))
console.log( area( {name: "square", width: 40, height: 50}))


