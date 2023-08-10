var images = document.getElementsByClassName("full-screen");

if (images) {
    for (let image of images) {
        image.addEventListener('click', function (e) {
            image.requestFullscreen();
        })

        image.addEventListener('click', function (e) {
            document.exitFullscreen();
        })
    }
}