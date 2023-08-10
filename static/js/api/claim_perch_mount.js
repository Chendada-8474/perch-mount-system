var button = document.getElementById("submitClaimBy");
var claimPerchMountButtons = document.getElementsByClassName("claim-perch-mount");
var unclaimPerchMountButtons = document.getElementsByClassName("unclaim-perch-mount");
var host = "http://127.0.0.1:5000"


if (button) {
    button.addEventListener("click", (event) => {
        var memberId = document.getElementById("member").value;

        var ans = confirm("確定要變更認領人嗎？");
        if (!ans) { return; }

        if (memberId) {
            fetch(host + `/api/claim_perch_mount/${event.target.value}/claim_by/${memberId}`, {
                method: "PUT",
            })
                .then(response => response)
                .then(response => {
                    location.reload();
                })
                .catch(err => alert(err));
            return;
        }
        fetch(host + `/api/claim_perch_mount/${event.target.value}`, {
            method: "DELETE",
        })
            .then(response => response)
            .then(response => {
                location.reload();
            })
            .catch(err => alert(err));
    })
}

if (claimPerchMountButtons) {
    for (var button of claimPerchMountButtons) {
        button.addEventListener("click", (event) => {
            var memberId = document.getElementById("member").value;

            var ans = confirm("確定要認領嗎？");
            if (!ans) { return; }

            fetch(host + `/api/claim_perch_mount/${event.target.value}/claim_by/${memberId}`, {
                method: "PUT",
            })
                .then(response => response)
                .then(response => {
                    location.reload();
                })
                .catch(err => alert(err));
            return;

        })
    }
}

if (unclaimPerchMountButtons) {
    for (var button of unclaimPerchMountButtons) {
        button.addEventListener("click", (event) => {

            var ans = confirm("確定要取消認領嗎？");
            if (!ans) { return; }

            fetch(host + `/api/claim_perch_mount/${event.target.value}`, {
                method: "DELETE",
            })
                .then(response => response)
                .then(response => {
                    location.reload();
                })
                .catch(err => alert(err));
            return;

        })
    }
}