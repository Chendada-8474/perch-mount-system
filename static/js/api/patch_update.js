var updateButtons = document.getElementsByClassName("update");

for (var button of updateButtons) {
    button.addEventListener("click", (event) => {
        var updateInfoId = event.target.value;
        fetch(`/api/update_info/${updateInfoId}`, { method: "delete", })
            .then(response => response)
            .then(response => { location.reload(); })
            .catch(err => alert(err));
    })
}