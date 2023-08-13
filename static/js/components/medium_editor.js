var openEditorButtons = document.getElementsByClassName("open-medium-editor");
var modalTitle = document.getElementById("currentMediumId");
var modalImage = document.getElementById("editModalImage");
var modalVideo = document.getElementById("editModalVideo");
var individualTbody = document.getElementById("individualInfo");

var mediumDatetimeSpan = document.getElementById("mediumDatetimeIfo");
var sectionSpan = document.getElementById("sectionInfo");
var eventSpan = document.getElementById("eventInfo");
var featuredBehaviorSpan = document.getElementById("featuredBehaviorInfo");
var pathSpan = document.getElementById("pathInfo");
var reviewerSpan = document.getElementById("reviewerInfo");
var emptyCheckerSpan = document.getElementById("emptyCheckerInfo");
var featuredBySpan = document.getElementById("featuredByInfo");


for (var openButton of openEditorButtons) {
    openButton.addEventListener("click", (event) => {

        fetch(`/api/medium/${event.currentTarget.value}`, { method: "GET" })
            .then(response => response.json())
            .then(response => {
                initMedium(response);
            })
            .catch(err => alert(err));

        fetch(`/api/medium/${event.currentTarget.value}/individuals`, { method: "GET" })
            .then(response => response.json())
            .then(response => {
                initIndividuals(response);
            })
            .catch(err => alert(err));
    })

}

function initMedium(medium) {
    modalTitle.innerHTML = medium.medium_id;
    initMediumInfo(medium);
    if (medium.is_image) {
        modalImage.src = host + `/uploads/${medium.path}`;
        modalImage.style.display = "block";
        modalVideo.style.display = "none";
    } else {
        modalVideo.src = host + `/uploads/${medium.path}`;
        modalVideo.style.display = "block";
        modalImage.style.display = "none";
    }
}

function initIndividuals(individuals) {
    individualTbody.innerHTML = "";
    for (var individual of individuals) {
        individualTbody.appendChild(individualTr(individual));
    }
    feather.replace();
}


function individualTr(individual) {
    var tr = document.createElement("tr");
    var td = `
        <th scope="row">${individual.individual_id}</th>
        <td>${(individual.ai_species) ? individual.ai_species : ""}</td>
        <td>${(individual.species) ? individual.species : ""}</td>
        <td>${(individual.tagged) ? '<i data-feather="check"></i>' : ""}</td>
        <td>${(individual.ring_number) ? individual.ring_number : ""}</td>
        <td>${(individual.prey) ? '<i data-feather="check"></i>' : ""}</td>
        <td>${(individual.prey_name) ? individual.prey_name : ""}</td>
        <td>
            <button type="button" class="btn btn-link btn-sm open-individual-editor" data-bs-toggle="modal" data-bs-target="#individualEditerModal" value="${individual.individual_id}">
            <i data-feather="edit"></i>
            </button>
        </td>
        <td>
            <button type="button" class="btn btn-link btn-sm open-individual-editor" data-bs-toggle="modal" data-bs-target="#individualEditerModal" value="${individual.individual_id}">
            <i data-feather="trash-2"></i>
            </button>
        </td>
    `
    tr.innerHTML = td;
    var buttons = tr.getElementsByClassName("open-individual-editor")
    for (var button of buttons) {
        button.addEventListener("click", (event) => {
            var individualId = event.currentTarget.value;
            console.log(individualId)
        });
    }

    return tr;
}


function initMediumInfo(medium) {
    mediumDatetimeSpan.innerHTML = medium.medium_datetime;
    sectionSpan.innerHTML = medium.section;
    eventSpan.innerHTML = (medium.event) ? medium.event : "";
    featuredBehaviorSpan.innerHTML = (medium.featured_behavior) ? medium.featured_behavior : "";
    pathSpan.innerHTML = medium.path;
    reviewerSpan.innerHTML = medium.reviewer;
    emptyCheckerSpan.innerHTML = (medium.empty_checker) ? medium.empty_checker : "";
    featuredBySpan.innerHTML = (medium.featured_by) ? medium.featured_by : "";
}