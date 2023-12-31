var preyInputs = document.getElementsByClassName("prey");
var indentifer = document.getElementById("identiferId").value;


if (preyInputs) {
    for (var preyInput of preyInputs) {
        preyInput.addEventListener("focusout", (event) => {

            var individualId = event.target.parentNode.querySelector("input[name='individual_id']").value;
            var preyName = (event.target.value) ? event.target.value : null;

            fetch(`/api/prey/${individualId}`, {
                method: "PUT",
                body: JSON.stringify({
                    "prey_name": preyName,
                    "prey_identify_by": indentifer,
                }),
                headers: new Headers({
                    "Content-Type": "application/json",
                })
            })
                .then(response => response)
                .then(response => { })
                .catch(err => alert(err));
        })
    }
}