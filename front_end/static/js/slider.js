let protein_slider = document.getElementById("protein_slider");
let protein_box = document.getElementById("protein_box");

let fiber_slider = document.getElementById("fiber_slider");
let fiber_box = document.getElementById("fiber_box");

protein_slider.addEventListener("change", function (event) {
    protein_box.value = this.value;
});

let carb_slider = document.getElementById("carb_slider");
let carb_box = document.getElementById("carb_box");

carb_slider.addEventListener("change", function (event) {

    if (carb_slider.value <= fiber_slider.value) {
        fiber_slider.value = carb_slider.value;
        fiber_box.value = carb_slider.value
    }
        carb_box.value = this.value;


});


fiber_slider.addEventListener("change", function (event) {
    carb_slider = document.getElementById("carb_slider");

    if (fiber_slider.value >= carb_slider.value) {
        console.log("inside box")
        carb_slider.value = fiber_slider.value;
        carb_box.value = fiber_slider.value;
    }
    fiber_box.value = this.value;
});

let fat_box = document.getElementById("fat_box");
let fat_slider = document.getElementById("fat_slider");

fat_slider.addEventListener("change", function (event) {

    fat_box.value = this.value;
});