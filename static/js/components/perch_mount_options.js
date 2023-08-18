var projectSelect = document.getElementById("project");
var perchMountSelect = document.getElementById("perch_mount")
var perchMountMap = {};

fetch("/api/perch_mounts", {
    method: "GET"
})
    .then(response => response.json())
    .then(response => {
        for (var perchMount of response) {
            if (perchMountMap[perchMount.project_id] == undefined) {
                perchMountMap[perchMount.project_id] = [];
            }
            perchMountMap[perchMount.project_id].push(
                {
                    "perch_mount_id": perchMount.perch_mount_id,
                    "perch_mount_name": perchMount.perch_mount_name,
                }
            )
        }
    })
    .catch(err => alert(err));


projectSelect.addEventListener("input", (event) => {
    var values = [];
    for (var option of projectSelect.children) {
        if (option.selected) {
            values.push(option.value);
        }
    }

    perchMountSelect.innerHTML = "";
    for (var project_id of values) {
        for (var perchMount of perchMountMap[project_id]) {
            var option = document.createElement("option");
            option.innerHTML = `${perchMount.perch_mount_id}. ${perchMount.perch_mount_name}`;
            option.value = perchMount.perch_mount_id;
            perchMountSelect.appendChild(option);
        }
    }

})
