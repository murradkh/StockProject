var recent_time_range_chose;
var recent_symbol_to_compare;
var myLineChart;

function getHistoricData(symbol,time_range='1m', symbol_to_compare = '') {
    recent_time_range_chose = time_range;
    if(typeof(recent_symbol_to_compare) !== 'undefined' && symbol_to_compare == ''){
    symbol_to_compare = recent_symbol_to_compare;
    }
    $.get(`/historic/${symbol},${symbol_to_compare}/${time_range}/`, function(data,received, response) {
        if (response.status == 200) {
            if (typeof(myLineChart) !== 'undefined') {
            //removing old chart
            myLineChart.destroy();
        }
            var ctxL = document.getElementById("stockChart").getContext('2d');
            datasets = []

            if (symbol_to_compare == '' || symbol_to_compare == symbol) {
                historic_data_1 = data.data.sort(function(a, b) {
                    return a.date - b.date;
                })
            } else {
                historic_data_1 = data.data[symbol]['chart'].sort(function(a, b) {
                    return a.date - b.date;
                })
                historic_data_2 = data.data[symbol_to_compare]['chart'].sort(function(a, b) {
                    return a.date - b.date;
                })


            var colors = getRandomRgba();
            datasets.push({
                label: `${symbol_to_compare}`,
                data: historic_data_2.map(d => d.close),
                                backgroundColor: [colors[0]],
                                borderColor: [colors[1]],
                                borderWidth: 2
            })
            }
            var colors = getRandomRgba();
            datasets.push({
                label: `${symbol}`,
                data: historic_data_1.map(d => d.close),
                                backgroundColor: [colors[0]],
                                borderColor: [colors[1]],
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

function compareTwoStocks(originSymbol) {
    var stockNameOption = document.forms["compareForm"]['stockNameToCompare']['value'];
    if (stockNameOption != '') {
        secondarySymbol = stockNameOption.slice(0, stockNameOption.indexOf(','))
        getHistoricData(originSymbol,recent_time_range_chose ,secondarySymbol);
        recent_symbol_to_compare = secondarySymbol;
    }
}
