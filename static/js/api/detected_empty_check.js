var sendButton = document.getElementById("sendButton");
var media = document.getElementsByClassName("empty-medium");
var perchMountId = document.getElementById("perchMountId").value;
var sectionId = document.getElementById("sectionId").value;


sendButton.addEventListener("click", (event) => {
    var emptyMedia = [];
    var mediaIds = [];

    for (var medium of media) {
        var isEmpty = medium.querySelector("input[name='false_nagetve']").checked;
        if (isEmpty) {
            emptyMedia.push(
                {
                    "detected_medium_id": medium.id,
                    "path": medium.querySelector("input[name='path']").value,
                }
            )
        }
        mediaIds.push(medium.id);
    }

    var ans = confirm(`確定要送出資料嗎？\n你選擇了：${emptyMedia.length} 個空拍檔案。`);
    if (!ans) {
        return;
    }


    fetch("/api/review", {
        method: "DELETE",
        body: JSON.stringify({ "media": emptyMedia }),
        headers: new Headers({
            "Content-Type": "application/json",
        })
    })
        .then(response => response.json())
        .then(response => {

            if (response.message) {
                alert("你重複檢視了一樣的資料，網頁將把你導回首頁。")
                window.location.replace(`/perch_mount/${perchMountId}`);
            }
        })
        .catch(err => {
            alert(err);
            window.location.replace(`/perch_mount/${perchMountId}`);
        });

    fetch("/api/empty_check_detected", {
        method: "PATCH",
        body: JSON.stringify({ "medium_ids": mediaIds }),
        headers: new Headers({ "Content-Type": "application/json" })
    })
        .then(response => response.json())
        .then(response => {
            window.location.replace(`/perch_mount/${perchMountId}`);
        })
        .catch(err => {
            alert(err);
            window.location.replace(`/perch_mount/${perchMountId}`);
        });
})