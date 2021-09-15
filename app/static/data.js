$(document).ready(() => {
    $.ajax({
        type: "GET",
        url: "../static/repo_list10.json",
        dataType: "json"
    })
        .done((res) => {
            console.log(res);
        })
})