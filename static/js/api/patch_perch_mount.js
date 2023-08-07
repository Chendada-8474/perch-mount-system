var host = "http://127.0.0.1:5000"


window.addEventListener('load', function () {
    var terminateButton = document.getElementById("terminatePerchMount");
    var resetButton = document.getElementById("resetPerchMount");

    if (terminateButton) {
        terminateButton.addEventListener("click", (event) => {
            var ans = confirm("確定要撤收這支棲架嗎？");
            if (!ans) { return; }
            var api_url = `/api/perch_mount/${event.target.value}`

            fetch(host + api_url, {
                method: "PATCH",
                body: JSON.stringify({ 'terminated': true }),
                headers: new Headers({
                    "Content-Type": "application/json",
                })
            })
                .then(response => response)
                .then(response => { location.reload(); })
                .catch(err => alert(err));
        })
    }

    if (resetButton) {
        resetButton.addEventListener("click", (event) => {
            var ans = confirm("確定要恢復這支棲架嗎？");
            if (!ans) { return; }
            var api_url = `/api/perch_mount/${event.target.value}`
            fetch(host + api_url, {
                method: "PATCH",
                body: JSON.stringify({ 'terminated': false }),
                headers: new Headers({
                    "Content-Type": "application/json",
                })
            })
                .then(response => response)
                .then(response => { location.reload(); })
                .catch(err => alert(err));
        })
    }
})