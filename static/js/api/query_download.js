var project = document.getElementById("project");
var perchMount = document.getElementById("perch_mount");
var species = document.getElementById("species");
var startTime = document.getElementById("start_time");
var endTime = document.getElementById("end_time");
var raptor = document.getElementById("raptor");
var prey = document.getElementById("prey");
var identifiedPrey = document.getElementById("identified_prey");
var tagged = document.getElementById("tagged");
var submit = document.getElementById("submit");

var downloadRowData = document.getElementById("downloadRowData");
var downloadSpeciesList = document.getElementById("downloadSpeciesList");

var rowDataTbody = document.getElementById("rowDataTbody");
var speciesListTbody = document.getElementById("speciesListTbody");
var numData = document.getElementById("numData");
var loading = document.getElementById("loading");


var rowData = [];

downloadSpeciesList.addEventListener("click", (event) => {

    var csv = toCsv(document.getElementById("speciesListTable"));
    downloadCsv(csv, "species_list.csv");
})

downloadRowData.addEventListener("click", (event) => {
    buildData(rowData).then(data => downloadJSONToCSV(data));
})




submit.addEventListener("click", (event) => {
    if (!project.value && !perchMount.value && !species.value && !startTime.value && !endTime.value && !raptor.value) {
        alert("請輸入參選條件");
    }

    var projects = getMultipleValues(project)
    var perchMounts = getMultipleValues(perchMount)
    var AllSpecies = getMultipleValues(species)

    var data = {
        "project": (projects) ? project : null,
        "perch_mount": (perchMounts) ? perchMounts : null,
        "species": (AllSpecies) ? AllSpecies : null,
        "start_time": (startTime.value) ? startTime.value : null,
        "end_time": (endTime.value) ? endTime.value : null,
        "raptor": (raptor.value) ? raptor.value : null,
        "prey": prey.checked,
        "identified_prey": identifiedPrey.checked,
        "tagged": tagged.checked,
    }

    rowDataTbody.innerHTML = "";
    speciesListTbody.innerHTML = "";

    loading.classList.remove("d-none");

    fetch("/api/query_data", {
        method: "POST",
        body: JSON.stringify(data),
        headers: new Headers({
            "Content-Type": "application/json",
        })
    })
        .then(response => response.json())
        .then(response => {
            makeTable(response);
        })
        .catch(err => alert(err));

})


function makeTable(data) {
    rowData = [];
    numData.innerHTML = data.row_data.length;
    var count = 50;
    for (var individual of data.row_data) {
        if (count > 0) {
            var tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${individual.taxon_order}</td>
                <td>${individual.species}</td>
                <td>${individual.project}</td>
                <td>${individual.perch_mount}</td>
                <td>${individual.medium_datetime}</td>
                <td>${individual.prey}</td>
                <td>${(individual.prey_name) ? individual.prey_name : ""}</td>
                <td>${individual.tagged}</td>
                <td>${(individual.ring_number) ? individual.ring_number : ""}</td>
            `
            rowDataTbody.appendChild(tr);
        }
        rowData.push(individual);
        count -= 1;
    }


    for (var species of data.species_list) {

        var tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${species.species}</td>
            <td class="fst-italic">${species.scientific_name}</td>
            <td>${species.english_common_name}</td>
            <td>${species.family_latin_name}</td>
            <td>${(species.taiwan_status) ? species.taiwan_status : ""}</td>
            <td>${(species.endemism) ? species.endemism : ""}</td>
            <td>${(species.conservation_status) ? species.conservation_status : ""}</td>
        `
        count -= 1;
        speciesListTbody.appendChild(tr);
    }

    loading.classList.add("d-none")
}

function getMultipleValues(select) {
    var values = [];
    for (var option of select.children) {
        if (option.selected) {
            values.push(option.value);
        }
    }
    return values;
}





const toCsv = function (table) {
    // Query all rows
    const rows = table.querySelectorAll('tr');

    return [].slice
        .call(rows)
        .map(function (row) {
            // Query all cells
            const cells = row.querySelectorAll('th,td');
            return [].slice
                .call(cells)
                .map(function (cell) {
                    return cell.textContent;
                })
                .join(',');
        })
        .join('\n');
};

const downloadCsv = function (text, fileName) {
    const link = document.createElement('a');
    link.setAttribute('href', `data:text/csv;charset=utf-8,${encodeURIComponent(text)}`);
    link.setAttribute('download', fileName);

    link.style.display = 'none';
    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);
};


const buildData = data => {

    return new Promise((resolve, reject) => {

        // 最後所有的資料會存在這
        let arrayData = [];

        // 取 data 的第一個 Object 的 key 當表頭
        let arrayTitle = Object.keys(data[0]);
        arrayData.push(arrayTitle);

        // 取出每一個 Object 裡的 value，push 進新的 Array 裡
        Array.prototype.forEach.call(data, d => {
            let items = [];
            Array.prototype.forEach.call(arrayTitle, title => {
                let item = d[title] || '無';
                items.push(item);
            });
            arrayData.push(items)
        })

        resolve(arrayData);
    })

}

const downloadJSONToCSV = data => {
    let csvContent = '';
    Array.prototype.forEach.call(data, d => {
        let dataString = d.join(',') + '\n';
        csvContent += dataString;
    })

    // 下載的檔案名稱
    let fileName = 'row_data_' + (new Date()).getTime() + '.csv';

    // 建立一個 a，並點擊它
    let link = document.createElement('a');
    link.setAttribute('href', 'data:text/csv;charset=utf-8,%EF%BB%BF' + encodeURI(csvContent));
    link.setAttribute('download', fileName);
    link.click();
}