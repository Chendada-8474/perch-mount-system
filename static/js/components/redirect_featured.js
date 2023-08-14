var redirectButton = document.getElementById("redirectFeatured");

redirectButton.addEventListener("click", (event) => {
    var perch_mount_name = document.getElementById("perchMount").value;
    var behavior = document.getElementById("behavior").value;
    var chinese_common_name = document.getElementById("species").value;
    var member = document.getElementById("member").value;

    perch_mount_name = (perch_mount_name) ? perch_mount_name : "$";
    chinese_common_name = (chinese_common_name) ? chinese_common_name : "$";

    window.location.href = `/featured/page/0/perch_mount/${perch_mount_name}/behavior/${behavior}/species/${chinese_common_name}/member/${member}`

})