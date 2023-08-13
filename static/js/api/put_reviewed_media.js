var sendButton = document.getElementById("confirm-send-button")
var media = document.getElementById("contents").children
var perchMountId = document.getElementById("perchMountId").value;
var reviewerId = document.getElementById("current_user").value;

sendButton.addEventListener("click", (event) => {
    var reviewedMedia = [];
    var emptyMedia = [];

    for (var medium of media) {
        var medium_id = medium.id;
        var section = medium.querySelector("input[name='section']").value;
        var medium_datetime = medium.querySelector("input[name='medium_datetime']").value;
        var path = medium.querySelector("input[name='path']").value;
        var empty_checker = medium.querySelector("input[name='empty_checker']").value;
        var event = medium.querySelector("select[name='event']").value;
        var featured_title = medium.querySelector("input[name='feature_title']").value;
        var featured_behavior = medium.querySelector("input[name='feature_behavior']").value;
        var individuals = medium.querySelector("tbody").children;

        if (!individuals.length && !featured_behavior && !event) {
            emptyMedia.push({
                "detected_medium_id": medium_id,
                "path": path
            });
            continue;
        }

        var reviewedMedium = {
            "detected_medium_id": medium_id,
            "section": section,
            "medium_datetime": medium_datetime,
            "path": path,
            "empty_checker": (empty_checker) ? empty_checker : null,
            "reviewer": reviewerId,
            "event": (event) ? event : null,
            "featured_title": (featured_title) ? featured_title : null,
            "featured_by": (featured_behavior) ? reviewerId : null,
            "featured_behavior": (featured_behavior) ? featured_behavior : null,
            "individuals": []
        }

        for (var individaul of individuals) {
            var taxon_order_by_ai = individaul.querySelector("input[name='taxon_order_by_ai']").value;
            var taxon_order_by_human = individaul.querySelector("input[name='taxon_order_by_human']").value;
            var prey = individaul.querySelector("input[name='prey']").checked;
            var tagged = individaul.querySelector("input[name='tagged']").checked;
            var ring_number = individaul.querySelector("input[name='ring_number']").value;
            var xmin = individaul.querySelector("input[name='xmin']").value;
            var xmax = individaul.querySelector("input[name='xmax']").value;
            var ymin = individaul.querySelector("input[name='ymin']").value;
            var ymax = individaul.querySelector("input[name='ymax']").value;

            reviewedMedium.individuals.push({
                "taxon_order_by_ai": (taxon_order_by_ai) ? taxon_order_by_ai : null,
                "taxon_order_by_human": taxon_order_by_human,
                "prey": (prey) ? prey : null,
                "tagged": (tagged) ? tagged : null,
                "ring_number": (ring_number) ? ring_number : null,
                "xmin": (xmin) ? xmin : null,
                "xmax": (xmax) ? xmax : null,
                "ymin": (ymin) ? ymin : null,
                "ymax": (ymax) ? ymax : null,
            })
        }
        reviewedMedia.push(reviewedMedium);
    }


    var api_url = "/api/review"
    fetch(api_url, {
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


    fetch(api_url, {
        method: "PUT",
        body: JSON.stringify({ "media": reviewedMedia }),
        headers: new Headers({
            "Content-Type": "application/json",
        })
    })
        .then(response => response.json())
        .then(response => {

            if (response.message) {
                alert("你重複檢視了一樣的資料，網頁將把你導回棲架頁面。")
                window.location.replace(`/perch_mount/${perchMountId}`);
            }
        })
        .catch(err => {
            alert(err)
            window.location.replace(`/perch_mount/${perchMountId}`);
        });

    fetch("/api/contribution", {
        method: "POST",
        body: JSON.stringify({
            "contributor": reviewerId,
            "num_files": reviewedMedia.length + emptyMedia.length,
            "action": 2
        }),
        headers: new Headers({
            "Content-Type": "application/json",
        })
    })
        .then(response => response.json())
        .then(response => { })
        .catch(err => {
            alert(err);
            window.location.replace(`/perch_mount/${perchMountId}`);
        });
    alert("資料已成功送出！");
    window.location.replace(`/perch_mount/${perchMountId}`);
})