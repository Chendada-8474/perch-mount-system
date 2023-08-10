var downloadButtons = document.getElementsByClassName("download-medium");

for (var button of downloadButtons) {
    button.addEventListener("click", (event) => {
        location.href = `/download_medium/${event.currentTarget.value}`;
    })
}