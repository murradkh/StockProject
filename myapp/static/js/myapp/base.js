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


function getUnreadCount(){
    badge = document.getElementById('badgeCounter');
    badge.innerHTML = "";
    var xhr = new XMLHttpRequest();
    var url = myapp.URLS.notificationsUnreadCount;
    xhr.open("GET", url, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            var status = xhr.status;
            if (status === 0 || (status >= 200 && status < 400)) {
                var responseDict = JSON.parse(xhr.responseText);
                var numNotifications = responseDict['unread_count']
                if (numNotifications > 0){      
                    badge.appendChild(document.createTextNode(numNotifications));
                }
            }
        }
    };
    xhr.send();
}


$("#notificationsDropdown").on("show.bs.dropdown", function getNotifications(){
    var xhr = new XMLHttpRequest();
    var url = myapp.URLS.listNotifications;
    xhr.open("GET", url, true);

    nContainer = document.getElementById('notificationsContainer');
    nContainer.innerHTML = "";

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
                    nContainer.prepend(paragraph);
                }
                else {
                    for (var key in responseDict) {
                        if (responseDict.hasOwnProperty(key)) {
                            var link = document.createElement("a");
                            link.href = responseDict[key]['link'];
                            link.style.textDecoration = "none";

                            var div = document.createElement("div");
                            if (responseDict[key]['is_read']){
                                div.className = "alert alert-secondary";
                            }
                            else {
                                div.className = "alert alert-primary";
                            }
                            
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
                            nContainer.prepend(link);
                            div.onclick = function() { markAsRead(responseDict[key]['pk']); };
                        }
                    }
                }
            }
        }
    };
    xhr.send();
});


function markAsRead(pk=""){
    var xhr = new XMLHttpRequest();
    if (pk === "") {
        var url = myapp.URLS.notificationsAllRead; 
    }
    else {
        var url = `../../../../notifications/${pk}/nread/`
    }
    xhr.open("POST", url, true);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            var status = xhr.status;
            if (status === 0 || (status >= 200 && status < 400)) {
                console.log("all read");
            }
        }
    };
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    xhr.send();
    getUnreadCount();
    getNotifications();
}


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
                console.log("all deleted");
            }
        }
    };
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    xhr.send();
    getUnreadCount();
    getNotifications();
}


function parseDateTime(isoFormat) {
    date = new Date(isoFormat);
    return date.toDateString() + " at " + date.toLocaleTimeString().substr(0, 5);
}
