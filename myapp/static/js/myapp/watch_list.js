 function watchlistRemove(symbol, number) {
        var row = document.getElementById("row" + number);

        var xhr = new XMLHttpRequest();
        xhr.open("POST", `../../stock/${symbol}/wremove/`, true);

        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                var status = xhr.status;
                // In local files, status is 0 upon success
                if (status === 0 || (status >= 200 && status < 400)) {
                    row.parentNode.removeChild(row);

                    var table = document.getElementById('stockstable');
                    var rowCount = table.rows.length;

                    if (rowCount == "1"){
                        table.innerHTML="Your watchlist is currently empty";
                    }
                }
            }
        };
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        xhr.send();
    }

 function startInterval(time, path){
    setInterval(function() {
  if ($('#customSwitch1').is(":checked")){
            $.ajax({
            method: "GET",
            url: path,
            success: function(data) {
                $('#stockstable').replaceWith($('#stockstable',data));
                document.getElementById("timer").innerHTML =new Date().toLocaleString();
                $("#timer").fadeTo(100, 0.1).fadeTo(200, 1.0);
            },
            error: function(data) {
                console.log("error")
            }
    })
    }
    }, time)
    }



