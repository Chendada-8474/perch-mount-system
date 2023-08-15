var updateButtons = document.getElementsByClassName("update");

for (var button of updateButtons) {
    button.addEventListener("click", (event) => {
        var updateInfoId = event.target.value;
        fetch(`/api/update_info/${updateInfoId}`, {
            method: "PATCH",
            body: JSON.stringify({ 'checked': true }),
            headers: new Headers({ "Content-Type": "application/json" })
        })
            .then(response => response)
            .then(response => { location.reload(); })
            .catch(err => alert(err));
    })
}