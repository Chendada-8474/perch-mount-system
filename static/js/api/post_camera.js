var newMemberButton = document.getElementById("submit");

newMemberButton.addEventListener("click", (event) => {
    var model_name = document.getElementById("model_name").value;

    fetch("/api/camera", {
        method: "POST",
        body: JSON.stringify({
            "model_name": model_name,
        }),
        headers: new Headers({
            "Content-Type": "application/json",
        })
    })
        .then(response => response)
        .then(response => {
            alert("新增成功")
            location.reload();
        })
        .catch(err => alert(err));
})