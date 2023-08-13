

window.addEventListener('load', function () {
    var terminateButton = document.getElementById("terminatePerchMount");
    var resetButton = document.getElementById("resetPerchMount");
    var coordinateButton = document.getElementById("submitCoordinate");
    var projectButton = document.getElementById("submitProject");
    var habitatButton = document.getElementById("submitHabitat");

    if (terminateButton) {
        terminateButton.addEventListener("click", (event) => {
            var ans = confirm("確定要撤收這支棲架嗎？");
            if (!ans) { return; }
            var api_url = `/api/perch_mount/${event.target.value}`

            fetch(api_url, {
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
            fetch(api_url, {
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

    if (coordinateButton) {
        coordinateButton.addEventListener("click", (event) => {
            var ans = confirm("確定要變更座標嗎？");
            if (!ans) { return; }
            var api_url = `/api/perch_mount/${event.target.value}`
            var latitude = document.getElementById("latitude").value;
            var longitude = document.getElementById("longitude").value;

            if (!latitude || !longitude) {
                alert("座標值不能為空");
                return;
            }

            fetch(api_url, {
                method: "PATCH",
                body: JSON.stringify(
                    {
                        'latitude': latitude,
                        'longitude': longitude
                    }
                ),
                headers: new Headers({
                    "Content-Type": "application/json",
                })
            })
                .then(response => response)
                .then(response => { location.reload(); })
                .catch(err => alert(err));
        })
    }

    if (projectButton) {
        projectButton.addEventListener("click", (event) => {
            var ans = confirm("確定要變更計畫嗎？");
            if (!ans) { return; }
            var api_url = `/api/perch_mount/${event.target.value}`

            fetch(api_url, {
                method: "PATCH",
                body: JSON.stringify(
                    {
                        'project': document.getElementById("project").value
                    }
                ),
                headers: new Headers({
                    "Content-Type": "application/json",
                })
            })
                .then(response => response)
                .then(response => { location.reload(); })
                .catch(err => alert(err));
        })
    }

    if (habitatButton) {
        habitatButton.addEventListener("click", (event) => {
            var ans = confirm("確定要變更棲地嗎？");
            if (!ans) { return; }
            var api_url = `/api/perch_mount/${event.target.value}`

            fetch(api_url, {
                method: "PATCH",
                body: JSON.stringify(
                    {
                        'habitat': document.getElementById("habitat").value
                    }
                ),
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