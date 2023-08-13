var updateFeaturedButton = document.getElementById("updateFeatured");
var updateEventButton = document.getElementById("updateEvent");
var behavior = document.getElementById("featured_behavior");
var title = document.getElementById("featured_title");
var eventSelect = document.getElementById("event");
var currentUser = document.getElementById("current_user").value;

updateFeaturedButton.addEventListener("click", (event) => {

    var ans = confirm("確定要變更精選資訊嗎？");
    if (!ans) { return; }
    var api_url = `/api/medium/${event.target.value}`

    fetch(api_url, {
        method: "PATCH",
        body: JSON.stringify(
            {
                'featured_title': (behavior.value) ? title.value : null,
                'featured_behavior': (behavior.value) ? behavior.value : null,
                'featured_by': (behavior.value) ? currentUser : null,
                'event': (eventSelect.value) ? eventSelect.value : null,
            }
        ),
        headers: new Headers({
            "Content-Type": "application/json",
        })
    })
        .then(response => response)
        .then(response => { location.reload(); })
        .catch(err => alert(err));

})

updateEventButton.addEventListener("click", (event) => {
    var ans = confirm("確定要變更事件嗎？");
    if (!ans) { return; }
    var api_url = `/api/medium/${event.target.value}`

    fetch(api_url, {
        method: "PATCH",
        body: JSON.stringify(
            {
                'featured_title': (behavior.value) ? title.value : null,
                'featured_behavior': (behavior.value) ? behavior.value : null,
                'featured_by': (behavior.value) ? currentUser : null,
                'event': (eventSelect.value) ? eventSelect.value : null,
            }
        ),
        headers: new Headers({
            "Content-Type": "application/json",
        })
    })
        .then(response => response)
        .then(response => { window.location.reload() })
        .catch(err => alert(err));

})