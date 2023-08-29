
window.addEventListener('load', function () {
    var submitButton = document.getElementById("submit_project");

    submitButton.addEventListener("click", (event) => {
        var projectName = document.getElementById("name").value;

        if (!projectName) {
            return;
        }

        data = { "name": projectName };

        var ans = this.confirm(`確定要新增計畫： "${projectName}" 嗎？`);
        if (!ans) {
            return;
        }

        fetch("/api/project", {
            method: "POST",
            body: JSON.stringify(data),
            headers: new Headers({
                "Content-Type": "application/json",
            })
        })
            .then(response => response)
            .then(response => {
                window.location = "/";
            })
            .catch(err => alert(err));
    });

})