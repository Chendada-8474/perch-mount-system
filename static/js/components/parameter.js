
var elements = document.getElementsByClassName("parameter");
var perchMountDataList = document.getElementById("perch_mount_list");

var perchMountId = document.getElementById("perch_mount_id");
var perchMountName = document.getElementById("perch_mount_name");
var project = document.getElementById("project");
var checkDate = document.getElementById("check_date");
var camera = document.getElementById("camera");
var mountType = document.getElementById("mount_type");
var note = document.getElementById("note");
var valid = document.getElementById("valid");
var operators = document.getElementById("operators");
var startTime = document.getElementById("start_time");
var submit = document.getElementById("submit");

var code = document.getElementById("parameterYAML");

var perchMountMap = {}
var cameraMap = {}
var mountTypeMap = {}

for (let option of perchMountDataList.children) {
    var projectContent = option.innerHTML.split("_")[0];
    var perchMountContent = option.innerHTML.split("_")[1];
    perchMountMap[option.value] = { "project": projectContent, "perch_mount_name": perchMountContent };
}

for (let option of camera.children) {
    cameraMap[option.value] = option.innerHTML;
}

for (let option of mountType.children) {
    mountTypeMap[option.value] = option.innerHTML;
}

operators.values = function () {
    member_ids = [];
    first_names = [];
    for (let option of operators.children) {
        if (option.selected) {
            member_ids.push(option.value);
            first_names.push(option.innerHTML);
        }
    }
    return { "operators": member_ids, "first_names": first_names }
}


var content = `# 將 檔案放在要上傳的資料夾中\nperch_mount_id: \nperch_mount_name: ""\nproject: ""\ncheck_date: ${checkDate.value}\ncamera: ${camera.value}      # ${cameraMap[camera.value]}\nmount_type: ${mountType.value}  # ${mountTypeMap[mountType.value]}\nnote: null\nvalid: ${valid.checked}\noperators: []\nstart_time: null\n`
code.innerHTML = content;

perchMountId.addEventListener("input", (event) => {
    var findPerchMount = perchMountMap[event.target.value];
    perchMountName.value = (findPerchMount) ? findPerchMount.perch_mount_name : "";
    project.value = (findPerchMount) ? findPerchMount.project : "";
})

for (let element of elements) {
    element.addEventListener("input", (event) => {
        updateParameterCode()
    })
}


submit.addEventListener("click", (event) => {

    var alertMessage = [];

    if (!operators.values().operators.length) {
        alertMessage.push("請輸入回收人員！")
    }

    if (!perchMountName.value || !perchMountId.value) {
        alertMessage.push("棲架欄位不能為空！")
    }


    if (!checkDate.value) {
        alertMessage.push("回收日期不能為空！")
    }
    console.log(alertMessage)

    if (alertMessage.length) {
        alert(alertMessage.join("\n"))
    } else {
        downloadString(content, "text/yaml", `${perchMountName.value}_${checkDate.value}.yaml`)
    }

})


function updateParameterCode() {


    var operators_info = operators.values()

    content = `# 將 ${perchMountName.value}_${checkDate.value}.yaml 檔案放在要上傳的資料夾中\nperch_mount_id: ${perchMountId.value}\nperch_mount_name: "${perchMountName.value}"\nproject: "${project.value}"\ncheck_date: ${checkDate.value}\ncamera: ${camera.value}      # ${cameraMap[camera.value]}\nmount_type: ${mountType.value}  # ${mountTypeMap[mountType.value]}\nnote: ${(note.value) ? '"' + note.value + '"' : null}\nvalid: ${valid.checked}\noperators: [${operators_info.operators}]  # ${operators_info.first_names}`

    if (startTime.value) {
        var date = startTime.value.split("T")[0];
        var time = startTime.value.split("T")[1] + ":00";
        content += `\nstart_time: ${date} ${time}`
    } else {
        content += `\nstart_time: null`
    }

    code.innerHTML = content;
    hljs.highlightAll();

}

function downloadString(text, fileType, fileName) {
    var save_text = text + "\nuploaded: false"
    var blob = new Blob([save_text], { type: fileType });

    var a = document.createElement('a');
    a.download = fileName;
    a.href = URL.createObjectURL(blob);
    a.dataset.downloadurl = [fileType, a.download, a.href].join(':');
    a.style.display = "none";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1500);
}