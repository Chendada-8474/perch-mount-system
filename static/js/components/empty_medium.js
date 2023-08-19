var emptyMedia = document.getElementsByClassName("empty-medium");
var sendButton = document.getElementById("sendButton");
var checkerId = document.getElementById("checkerId").value;
var perchMountId = document.getElementById("perchMountId").value;

for (let medium of emptyMedia) {
    medium.classList.add("border");
    medium.classList.add("border-primary");
    medium.classList.add("border-0");
    medium.addEventListener("click", (event) => {
        var checked = clickCheckBox(event.currentTarget);
        selectedStyle(event.currentTarget, checked);
    })
}

function clickCheckBox(medium) {
    var checkBox = medium.querySelector("input[name='false_nagetve']");
    checkBox.checked = !checkBox.checked;
    return checkBox.checked;
}

function selectedStyle(medium, check) {
    if (check) {
        medium.classList.remove("border-0");
        medium.classList.add("border-4");
    } else {
        medium.classList.remove("border-4");
        medium.classList.add("border-0");
    }
}


sendButton.addEventListener("click", (event) => {
    var mediaWithAnimal = [];
    var trueEmptyMedia = [];

    for (let medium of emptyMedia) {
        var isThereAnimal = medium.querySelector("input[name='false_nagetve']").checked;
        if (isThereAnimal) {
            mediaWithAnimal.push({
                "empty_medium_id": medium.id,
                "section": medium.querySelector("input[name='section']").value,
                "medium_datetime": medium.querySelector("input[name='medium_datetime']").value,
                "path": medium.querySelector("input[name='path']").value,
                "empty_checker": checkerId
            });
        } else {
            trueEmptyMedia.push({
                "empty_medium_id": medium.id,
                "path": medium.querySelector("input[name='path']").value,
            })
        }
    }

    var ans = confirm(`確定要送出資料嗎？\n你選擇了：\n${mediaWithAnimal.length} 個有動物的檔案，\n${trueEmptyMedia.length} 個空拍檔案。`);
    var api_url = "/api/empty_check"
    if (ans) {
        fetch(api_url, {
            method: "DELETE",
            body: JSON.stringify({ "media": trueEmptyMedia }),
            headers: new Headers({
                "Content-Type": "application/json",
            })
        })
            .then(response => response.json())
            .then(response => {

                if (response.message) {
                    alert("你重複檢視了一樣的資料，網頁將把你導回首頁。")
                    window.location = `/perch_mount/${perchMountId}`;
                }
            })
            .catch(err => {
                alert(err);
                window.location = `/perch_mount/${perchMountId}`;
            });

        fetch(api_url, {
            method: "PUT",
            body: JSON.stringify({ "media": mediaWithAnimal }),
            headers: new Headers({
                "Content-Type": "application/json",
            })
        })
            .then(response => response.json())
            .then(response => {

                if (response.message) {
                    alert("你重複檢視了一樣的資料，網頁將把你導回棲架頁面。")
                    window.location = `/perch_mount/${perchMountId}`;
                }
            })
            .catch(err => {
                alert(err)
                window.location = `/perch_mount/${perchMountId}`;
            });

        fetch("/api/contribution", {
            method: "POST",
            body: JSON.stringify({
                "contributor": checkerId,
                "num_files": mediaWithAnimal.length + trueEmptyMedia.length,
                "action": 1
            }),
            headers: new Headers({
                "Content-Type": "application/json",
            })
        })
            .then(response => response.json())
            .then(response => { })
            .catch(err => {
                alert(err);
                window.location = `/perch_mount/${perchMountId}`;
            });
        alert("資料已成功送出！");
        window.location = `/perch_mount/${perchMountId}`;
    }
})