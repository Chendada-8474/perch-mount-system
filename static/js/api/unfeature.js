var unfeaturesButtons = document.getElementsByClassName("defeature");

for (var button of unfeaturesButtons) {
    button.addEventListener("click", (event) => {
        var ans = confirm("確定取消精選嗎？");
        if (!ans) { return; }
        var b = event.currentTarget;
        var mediumId = event.currentTarget.value;

        fetch(`/api/medium/${mediumId}/feature`, { method: "DELETE", })
            .then(response => response)
            .then(response => {
                b.classList.add("disabled");
                document.getElementById(mediumId).classList.add("opacity-50");
            })
            .catch(err => alert(err));

    })
}