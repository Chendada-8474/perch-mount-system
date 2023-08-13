var priorButtons = document.getElementsByClassName("prior-perch-mount");
var unpriorButtons = document.getElementsByClassName("unprior-perch-mount");


if (priorButtons) {
    for (var priorButton of priorButtons) {
        priorButton.addEventListener("click", (event) => {
            fetch(`/api/perch_mount/${event.target.value}`, {
                method: "PATCH",
                body: JSON.stringify({
                    "is_priority": true,
                }),
                headers: new Headers({
                    "Content-Type": "application/json",
                })
            })
                .then(response => response)
                .then(response => {
                    location.reload();
                })
                .catch(err => alert(err));
        })
    }
}

if (unpriorButtons) {
    for (var unpriorButton of unpriorButtons) {
        unpriorButton.addEventListener("click", (event) => {
            fetch(`/api/perch_mount/${event.target.value}`, {
                method: "PATCH",
                body: JSON.stringify({
                    "is_priority": false,
                }),
                headers: new Headers({
                    "Content-Type": "application/json",
                })
            })
                .then(response => response)
                .then(response => {
                    location.reload();
                })
                .catch(err => alert(err));

        })
    }
}