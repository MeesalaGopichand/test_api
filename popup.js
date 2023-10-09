
function ajaxcall(){
    url = "http://127.0.0.1:5000/get-status/54FZTT2"
    fetch (url).then(response => {
        return response.json();
    }).then(data => {
        var tag = data.tag;
        var rem = data.rem_days;
        var result = tag + " " + rem;
        document.getElementById("result").innerHTML = result;
    }).catch(err =>{
        console.log("err");
    })
}

ajaxcall();