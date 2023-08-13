var newIndividualButton = document.getElementById("newIndividual");
var mediumId = document.getElementById("medium_id").value;

newIndividualButton.addEventListener("click", (evnet) => {
    var ans = confirm("確定新增個體嗎？");
    if (!ans) { return; }
    var species = document.getElementById("newSpecies").value;

    fetch("/api/taxon_orders", {
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

            fetch(`/api/individual/at_medium/${mediumId}`, {
                method: "POST",
                body: JSON.stringify({ "taxon_order_by_human": results[0] }),
                headers: new Headers({
                    "Content-Type": "application/json",
                })
            })
                .then(response => response)
                .then(response => {
                    location.reload();
                })
                .catch(err => alert(err));

        });


})
