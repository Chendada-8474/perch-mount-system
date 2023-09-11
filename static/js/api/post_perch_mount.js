var perchMountNameInput = document.getElementById("perch_mount_name");
var latitudeInput = document.getElementById("latitude");
var longitudeInput = document.getElementById("longitude");
var projectSelect = document.getElementById("project");
var habitatSelect = document.getElementById("habitat");
var layerSelect = document.getElementById("layer");


window.addEventListener('load', function () {
    var postPerchMountButton = document.getElementById("submit_perch_mount");

    postPerchMountButton.addEventListener("click", (event) => {
        var api_url = "/api/perch_mount"
        data = getPerchMountData();
        fetch(api_url, {
            method: "POST",
            body: JSON.stringify(data),
            headers: new Headers({
                "Content-Type": "application/json",
            })
        })
            .then(response => response.json())
            .then(json => {
                window.location = "/";
            })
            .catch(err => alert(err));
    });

})

function getPerchMountData() {
    return {
        "perch_mount_name": perchMountNameInput.value,
        "latitude": latitudeInput.value,
        "longitude": longitudeInput.value,
        "project": projectSelect.value,
        "habitat": habitatSelect.value,
        "layer": layerSelect.value,
    };
}