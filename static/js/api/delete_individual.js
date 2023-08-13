var deleteIndividualButtons = document.getElementsByClassName("delete-individual");

for (var button of deleteIndividualButtons) {
    button.addEventListener("click", (evnet) => {
        var ans = confirm("確定刪除個體嗎？\n這個動作會把這個個體從資料庫中永久刪除。");
        if (!ans) { return; }

        fetch(`/api/individual/${evnet.currentTarget.value}`, { method: "DELETE", })
            .then(response => response)
            .then(response => {
                location.reload();
            })
            .catch(err => alert(err));
    })
}