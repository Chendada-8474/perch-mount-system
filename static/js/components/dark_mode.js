var isDark = true;

var darkSwitch = document.getElementById("darkMode");
var secondaryTexts = document.getElementsByClassName("text-light");

var darkModeCookie = getCookieByName("dark_mode");

if (!darkModeCookie) {
    document.cookie = "dark_mode=true";
}

darkSwitch.checked = darkModeCookie == "true";

var mode = (darkSwitch.checked) ? "dark" : "light";
document.documentElement.setAttribute("data-bs-theme", mode);


darkSwitch.addEventListener("input", (event) => {


    if (event.target.checked) {
        document.documentElement.setAttribute("data-bs-theme", "dark");
        document.cookie = "dark_mode=true";
    } else {
        document.documentElement.setAttribute("data-bs-theme", "light");
        document.cookie = "dark_mode=false";
    }

})




function getCookieByName(name) {
    return document.cookie
        .split("; ")
        .find((row) => row.startsWith(`${name}=`))
        ?.split("=")[1];
}