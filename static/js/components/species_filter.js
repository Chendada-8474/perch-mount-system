var filter = document.getElementById("speicesFilter");
var filtElements = document.getElementsByClassName("species-filt-target");


var speciesOptions = new Set()

for (var e of filtElements) {
    var sp = e.querySelector(".species").innerHTML;
    speciesOptions.add(sp);
}

for (var sp of speciesOptions) {
    var option = document.createElement("option");
    option.value = sp;
    option.innerHTML = sp;
    filter.appendChild(option);
}


filter.addEventListener("input", event => {
    var selectedSp = event.target.value;

    console.log(selectedSp)

    if (!selectedSp) {
        for (var e of filtElements) {
            e.style.display = 'table-row';
        }
        return;
    }

    for (var e of filtElements) {
        var sp = e.querySelector(".species");
        if (selectedSp != sp.innerHTML) {
            e.style.display = 'none';
        } else {
            e.style.display = 'table-row';
        }
    }

})