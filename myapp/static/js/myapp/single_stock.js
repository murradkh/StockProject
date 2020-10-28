	var myLineChart;
	function getHistoric(symbol, symbol_to_compare){
		$.get( `/historic/${symbol}/`, function( data ) {
			historic_data = data.data.sort(function(a, b) { return a.date - b.date; })
            var ctxL = document.getElementById("stockChart").getContext('2d');
            datasets =[
						{
							label: `${symbol}`,
							data: historic_data.map(d => d.close),
							backgroundColor: [
								'rgba(105, 0, 132, .2)',
							],
							borderColor: [
								'rgba(200, 99, 132, .7)',
							],
							borderWidth: 2
						}
					]
            if (typeof(symbol_to_compare) !== 'undefined'){
            $.get( `/historic/${symbol_to_compare}/`, function( data ) {
			historic_data = data.data.sort(function(a, b) { return a.date - b.date; })
            datasets.push({
							label: `${symbol_to_compare}`,
							data: historic_data.map(d => d.close),
							backgroundColor: [
								'rgba(0, 0, 255, .2)',
							],
							borderColor: [
								'rgba(0,0,255, .7)',
							],
							borderWidth: 2,
						})
			myLineChart = new Chart(ctxL, {
				type: 'line',
				data: {
					labels: historic_data.map(d => d.label),
					datasets: datasets
				},
				options: {
					responsive: true
				}
			});
			});
            }else{
			myLineChart = new Chart(ctxL, {
				type: 'line',
				data: {
					labels: historic_data.map(d => d.label),
					datasets: datasets
				},
				options: {
					responsive: true
				}
			});
			}

		});
    };

    function getStockNames(){
    		$.get( `/stocks/list_names/`, function( data ) {
    		dataList = $(myDatalist)
    for (let i = 0; i < data.stocks_names.length; i++) {
    dataList.append(`<option value='${data.stocks_names[i][0]}, ${data.stocks_names[i][1]}'>`)
}

});

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

    function compareTwoStocks(originSymbol){
        var stockNameOption = document.forms["compareForm"]['stockNameToCompare']['value'];
        if (stockNameOption != ''){
        if (typeof(myLineChart) !== 'undefined'){
            //removing old chart
            myLineChart.destroy();
        }
        secondarySymbol = stockNameOption.slice(0,stockNameOption.indexOf(','))
        getHistoric(originSymbol,secondarySymbol);
        }

    };