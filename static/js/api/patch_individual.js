var updateSpeciesButtons = document.getElementsByClassName("update-species");
var updateTagButtons = document.getElementsByClassName("update-tag");
var updatePreyButtons = document.getElementsByClassName("update-prey");
var host = "http://127.0.0.1:5000"

for (var speciesButton of updateSpeciesButtons) {
    speciesButton.addEventListener("click", (event) => {
        update(event.target.value);
    })
}

for (var tagButton of updateTagButtons) {
    tagButton.addEventListener("click", (event) => {
        update(event.target.value);
    })

}

for (var preyButton of updatePreyButtons) {
    preyButton.addEventListener("click", (event) => {
        update(event.target.value);
    })

}



function update(individualId) {
    var species = document.getElementById("species" + individualId).value;
    var prey = document.getElementById("prey" + individualId).checked;
    var prey_name = document.getElementById("prey_name" + individualId).value;
    var tagged = document.getElementById("tagged" + individualId).checked;
    var ring_number = document.getElementById("ring_number" + individualId).value;

    var data = {
        "prey": prey,
        "prey_name": (prey_name) ? prey_name : null,
        "tagged": tagged,
        "ring_number": (ring_number) ? ring_number : null,
    }


    if (species) {

        fetch("http://127.0.0.1:5000/api/taxon_orders", {
            method: "POST",
            body: JSON.stringify({
                "chinese_common_names": [species],
            }),
            headers: new Headers({
                "Content-Type": "application/json",
            })
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (results) {
                if (!results[0]) {
                    alert("你輸入的物種有誤")
                    return
                }
                data["taxon_order_by_human"] = results[0];
                postIndividual(data, individualId);
            });

        return;
    }
    data["taxon_order_by_human"] = null;
    postIndividual(data, individualId);
}


function postIndividual(data, individualId) {
    var ans = confirm("確定要變更個體資訊嗎？");
    if (!ans) { return; }
    var api_url = `/api/individual/${individualId}`

    fetch(host + api_url, {
        method: "PATCH",
        body: JSON.stringify(data),
        headers: new Headers({
            "Content-Type": "application/json",
        })
    })
        .then(response => response)
        .then(response => {
            location.reload();
        })
        .catch(err => alert(err));
}
