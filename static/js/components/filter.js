window.addEventListener('load', function () {
    var projectFilter = document.getElementById("project_filter");
    var filtTargets = document.getElementsByClassName("filt-target");


    projectFilter.addEventListener("input", event => {
        if (!event.target.value) {
            for (let element of filtTargets) {
                element.style.display = 'block';
            }
        } else {
            for (let element of filtTargets) {
                element.style.display = 'none';
            }
            var showTargets = document.getElementsByClassName(`project_${event.target.value}`);
            for (let element of showTargets) {
                element.style.display = 'block';
            }
        }
    })
})
