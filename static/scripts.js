// Update the current slider value
function updateSliderVal() {
    var slider = document.getElementById("myRange");
    var output = document.getElementById("output");
    output.innerHTML = slider.value;
}

function show_hide(btn) {
    btnpp = btn.parentNode.parentNode;
    ans_el = btnpp.getElementsByClassName("answer")[0];
    if(ans_el.hidden === true) {
        ans_el.hidden = false;
        btn.innerHTML = "-";
    } else {
        ans_el.hidden = true;
        btn.innerHTML = "+";
    }
}
