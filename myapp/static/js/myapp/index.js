    function watchlistEdit(symbol, number) {
        var icon = document.getElementById("eyeicon" + number);
        var editButton = document.getElementById("editbutton" + number);

        if (icon.className == "fa fa-eye") {
            var operation = "wadd";
        }
        else {
            var operation = "wremove";
        }

        var xhr = new XMLHttpRequest();
        xhr.open("POST", `stock/${symbol}/${operation}/`, true);

        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                var status = xhr.status;
                // In local files, status is 0 upon success
                if (status === 0 || (status >= 200 && status < 400)) {
                    if (operation == "wadd") {
                        icon.className = "fa fa-eye-slash";
                        editButton.className = "btn btn-outline-danger";
                    }
                    else {
                        icon.className = "fa fa-eye";
                        editButton.className = "btn btn-outline-primary";
                    }
                }
            }
        };
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        xhr.send();
    }

function getStockNames() {
      searchText = document.getElementById("searchText");
      dataList = $(myDatalist)

      // sending request to fetch stock names if the input isn't empty
      if (searchText.value != ''){
      $.get(`/stocks/list_names/${searchText.value}`, function(data) {

      // removing previous search results
      var e = document.querySelector("datalist");
      e.innerHTML = "";
      for (let i = 0; i < data.stocks_names.length; i++) {
            dataList.append(`<option value='${data.stocks_names[i].symbol}, ${data.stocks_names[i].companyName}'>`)
      }
    });
}
}


function startInterval(time, path){
 setInterval(function() {
    if ($('#customSwitch1').is(":checked")){

        $.ajax({
        method: "GET",
        url: path,
        success: function(data) {
            $('#stock_table').replaceWith($('#stock_table',data));
            $(".clickable-row").click(function() {
                window.location = $(this).data("href");
            });
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

 $(document).ready(function(){
                $('.clickable-row').click(function(){
                    window.location = $(this).data('href');
                });





            });


