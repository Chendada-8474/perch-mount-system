var newMemberButton = document.getElementById("submit");
var host = "http://127.0.0.1:5000"

newMemberButton.addEventListener("click", (event) => {
    var chinese_name = document.getElementById("chinese_name").value;

    fetch(host + "/api/behavior", {
        method: "POST",
        body: JSON.stringify({
            "chinese_name": chinese_name,
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