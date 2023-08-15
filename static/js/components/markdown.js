var markdonwDivs = document.getElementsByClassName("markdown");


for (var div of markdonwDivs) {
    var headers = div.querySelectorAll("h1, h2, h3, h4, h5, h6");
    var lis = div.querySelectorAll("li");

    for (var h of headers) {
        h.classList.add("fw-bold");
    }

    for (var li of lis) {
        li.classList.add("mb-1");
    }


}
