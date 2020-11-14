function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
        c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
        }
    }
    return "";
}

// view notifications
$("#notificationsDropdown").on("show.bs.dropdown", function(event){
    var xhr = new XMLHttpRequest();
    var url = '../../../../notifications/';
    xhr.open("GET", url, true);

    dropdown = document.getElementById('notificationsContainer');
    dropdown.innerHTML = "";

    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            var status = xhr.status;
            if (status === 0 || (status >= 200 && status < 400)) {
                var responseDict = JSON.parse(xhr.responseText);
                if (Object.keys(responseDict).length === 0) {
                    var paragraph = document.createElement("p");
                    paragraph.className = "text-center";
                    var text = document.createTextNode("No new notifications");
                    paragraph.appendChild(text);
                    dropdown.prepend(paragraph);
                }
                else {
                    for (var key in responseDict) {
                        if (responseDict.hasOwnProperty(key)) {
                            var link = document.createElement("a");
                            var div = document.createElement("div");
                            div.className = "alert alert-secondary";
                            div.innerHTML = `<button type="button" class="close" 
                                            onclick="deleteNotifications(${responseDict[key]['pk']})" 
                                            data-dismiss="alert">×</button>`;
                            var header = document.createElement("strong");
                            var title = document.createTextNode(responseDict[key]['title']);
                            var time = document.createElement("small");
                            var timestamp = document.createTextNode(parseDateTime(responseDict[key]['time']));
                            var description = document.createTextNode(responseDict[key]['description']);
                            
                            link.appendChild(div);
                            div.appendChild(header);
                            header.appendChild(title);
                            div.appendChild(document.createElement("br"));
                            div.appendChild(description);
                            div.appendChild(document.createElement("br"));
                            div.appendChild(time);
                            time.appendChild(timestamp);
                            dropdown.prepend(link);
                        }
                    }
                }
            }
        }
    };
    xhr.send();
});

function deleteNotifications(pk=""){
    var xhr = new XMLHttpRequest();
    if (pk === "") {
        var url = `../../../../notifications/nremove/`;
    }
    else {
        var url = `../../../../notifications/${pk}/nremove/`;
    }
    
    xhr.open("POST", url, true);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            var status = xhr.status;
            if (status === 0 || (status >= 200 && status < 400)) {
                console.log("success");
            }
        }
    };
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    xhr.send();
}

function parseDateTime(isoFormat) {
    date = new Date(isoFormat);
    return date.toDateString() + " at " + date.toLocaleTimeString().substr(0, 5);
}
