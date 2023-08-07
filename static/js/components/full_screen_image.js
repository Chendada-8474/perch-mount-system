var images = document.getElementsByClassName("full-screen");

for (let image of images) {
    image.addEventListener('click', function (e) {
        image.requestFullscreen();
    })

    image.addEventListener('click', function (e) {
        document.exitFullscreen();
    })
}