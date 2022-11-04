#![allow(dead_code)]

struct Point {
    x: f32,
    y: f32,
}

// Structs can be reused as fields of another struct
struct Rectangle {
    // A rectangle can be specified by where the top left and bottom right
    // corners are in space.
    top_left: Point,
    bottom_right: Point,
}

fn rect_area(r : Rectangle) -> f32 {
    let width = r.bottom_right.x - r.top_left.x;
    assert!(width >= 0.0);
    let height = r.bottom_right.y - r.top_left.y;
    assert!(height >= 0.0);
    width * height
}

fn main(){
    let r = Rectangle{top_left:Point{x:1.0, y:3.0}, bottom_right:Point{x:5.0,y:3.5}};
    let area = rect_area(r); 
    print!("{area}");
}
