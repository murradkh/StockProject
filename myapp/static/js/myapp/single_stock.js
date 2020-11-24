var recent_time_range_chose;
var colors_graph1;
var recent_symbols_to_compare=[];
var myLineChart;
var originSymbol;
var myLineChart;


function getHistoricData(time_range='1m' , update=false) {
    recent_time_range_chose = time_range;
    $.get(`/historic/${originSymbol},${recent_symbols_to_compare.toString()}/${time_range}/`, function(data,received,
    response) {
        if (response.status == 200) {
            if (typeof(myLineChart) !== 'undefined') {
            //removing old chart
            myLineChart.destroy();
        }
            var ctxL = document.getElementById("stockChart").getContext('2d');
            datasets = []

            if (recent_symbols_to_compare.length == 0) {
                historic_data_1 = data.data.sort(function(a, b) {
                    return a.date - b.date;
                })
            } else {
                historic_data_1 = data.data[originSymbol]['chart'].sort(function(a, b) {
                    return a.date - b.date;
                })
            }
                for (let i = 0; i < recent_symbols_to_compare.length; i++) {
                if(data.data[recent_symbols_to_compare[i]] !== undefined){
                  historic_data = data.data[recent_symbols_to_compare[i]]['chart'].sort(function(a, b) {
                    return a.date - b.date;
                })

                colors = getRandomRgba();
                datasets.push({
                    label: `${recent_symbols_to_compare[i]}`,
                    data: historic_data.map(d => d.close),
                                    backgroundColor: [colors[0]],
                                    borderColor: [colors[1]],
                                    borderWidth: 2
                })
            }
            }

            if (update==false){
            colors_graph1 = getRandomRgba();
            }
            datasets.push({
                label: `${originSymbol}`,
                data: historic_data_1.map(d => d.close),
                                backgroundColor: [colors_graph1[0]],
                                borderColor: [colors_graph1[1]],
                                borderWidth: 2
            })

//            console.log(historic_data_1)
            // For some strange reason, the 'today' data point returned by API has no label
            if (typeof historic_data_1[historic_data_1.length - 1].label === 'undefined') {
                    last_label = new Date(historic_data_1[historic_data_1.length -1].date).toString();
                    if (time_range == '3m' || time_range == '6m' || time_range.endsWith('y')){
                        historic_data_1[historic_data_1.length -1].label =
                            last_label.substr(3, 7) + ', '
                            + historic_data_1[historic_data_1.length -1].date.substr(2, 2);
                    }
                    else{
                        historic_data_1[historic_data_1.length -1].label = last_label.substr(3, 7);
                 }
            }
            myLineChart = new Chart(ctxL, {
            type: 'line',
            data: {
                labels: historic_data_1.map(d => d.label),
                datasets: datasets
            },
            options: {
                responsive: true,
                spanGaps: true,
            }
        });
            if(update==true){
                myLineChart.update(0);
            }

        }
    });
};
function getRandomRgba() {
        var o = Math.round, r = Math.random, s = 255;
        var color = 'rgba(' + o(r()*s) + ',' + o(r()*s) + ',' + o(r()*s)
        var backgroundColor = color + ',' + '0.2' + ')';
        var borderColor = color + ',' + '0.6' + ')';
        return [backgroundColor, borderColor];
    }

    function watchlistEdit() {
        var editButton = document.getElementById("editbutton");

        if (editButton.innerHTML.includes("Add to watchlist")) {
            var operation = "wadd";
        }
        else {
            var operation = "wremove";
        }

        var xhr = new XMLHttpRequest();
        xhr.open("POST", `${operation}/`, true);

        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                var status = xhr.status;
                // In local files, status is 0 upon success
                if (status === 0 || (status >= 200 && status < 400)) {
                    if (operation == "wadd") {
                        editButton.innerHTML = "<i class='fa fa-eye-slash'></i> Remove from watchlist";
                        editButton.className = "btn btn-outline-danger";
                    }
                    else {
                        editButton.innerHTML = "<i class='fa fa-eye'></i> Add to watchlist";
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
//      var element = document.getElementsByTagName("option");
//      for (index = element.length - 1; index >= 0; index--) {
//        element[index].parentNode.removeChild(element[index]);
//      }
      for (let i = 0; i < data.stocks_names.length; i++) {
            dataList.append(`<option value='${data.stocks_names[i].symbol}, ${data.stocks_names[i].companyName}'>`)
      }
    });
}
}

function addStockToCompare() {
    var stockNameOption = document.forms["compareForm"]['stockNameToCompare']['value'];
    secondarySymbol = stockNameOption.slice(0, stockNameOption.indexOf(','))
    if (stockNameOption != '' && secondarySymbol != originSymbol && !recent_symbols_to_compare.some(value => secondarySymbol == value)) {
        recent_symbols_to_compare.push(secondarySymbol);
        getHistoricData(recent_time_range_chose);
    }
}

function clearGraph(){
recent_symbols_to_compare = [];
getHistoricData(recent_time_range_chose)

}
function setOriginSymbol(symbol_name){
    originSymbol = symbol_name;
}

function startInterval(time, path){
 setInterval(function() {
        $.ajax({
        method: "GET",
        url: path,
        success: function(data) {
            $('#stock_data').replaceWith($('#stock_data',data));
            $('#text').replaceWith($('#text',data));
        },
        error: function(data) {
            console.log("error")
        }
    })
    }, time)


//    setInterval(function() {
//     if(recent_time_range_chose == '1d'){
//                getHistoricData("1d",true)
//    }
//    }, time)
    }
function multiply()
{
    qty = Number(document.getElementById('quantity').value);
    price = Number(document.getElementById('staticPrice').value);
    document.getElementById('staticTotal').value=Math.round(qty*price * 100) / 100;
}
function  validateForm()
{
  var total = Number(document.forms["buyForm"]["Total"].value);
  var budget = Number(document.getElementById('staticBudget').value);
  if (total > budget ) {
    alert("this process is above budget ");
    return false;

}
}
function reset (){
 $("#quantity")[0].reset()
}


