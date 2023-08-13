var newMemberButton = document.getElementById("submit");

newMemberButton.addEventListener("click", (event) => {
    var user_name = document.getElementById("user_name").value;
    var phone_number = document.getElementById("phone_number").value;
    var first_name = document.getElementById("first_name").value;
    var last_name = document.getElementById("last_name").value;
    var position = document.getElementById("position").value;

    fetch("/api/member", {
        method: "POST",
        body: JSON.stringify({
            "user_name": user_name,
            "phone_number": phone_number,
            "first_name": (first_name) ? first_name : null,
            "last_name": (last_name) ? last_name : null,
            "position": position,
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