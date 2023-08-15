


window.addEventListener('load', function () {
    var postPerchMountForm = document.getElementById("newPerchMount");

    postPerchMountForm.addEventListener("submit", (event) => {
        var api_url = "/api/perch_mount"
        data = formToJson(postPerchMountForm);
        fetch(api_url, {
            method: "POST",
            body: JSON.stringify(data),
            headers: new Headers({
                "Content-Type": "application/json",
            })
        })
            .then(response => response.json())
            .then(json => {
                window.location.replace(`/perch_mount/${json.perch_mount_id}`);
            })
            .catch(err => alert(err));
    });

})

function formToJson(form) {
    var data = {}
    for (let pair of new FormData(form)) {
        data[pair[0]] = (pair[1]) ? pair[1] : null;
    }
    return data;
}