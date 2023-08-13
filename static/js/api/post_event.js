var newMemberButton = document.getElementById("submit");

newMemberButton.addEventListener("click", (event) => {

    fetch("/api/event", {
        method: "POST",
        body: JSON.stringify({
            "chinese_name": document.getElementById("chinese_name").value,
            "english_name": document.getElementById("english_name").value,
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