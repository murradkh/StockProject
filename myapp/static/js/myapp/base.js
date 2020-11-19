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


function getNotifications(){
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
                            link.href = getAbsoluteURL(responseDict[key]['path']);
                            link.style.textDecoration = "none";

                            var div = document.createElement("div");
                            if (responseDict[key]['is_read']){
                                div.className = "alert alert-secondary";
                            }
                            else {
                                div.className = "alert alert-primary";
                            }
                            
                            div.innerHTML = `<button type="button" class="close" 
                                            onclick="deleteNotifications(${String(key)})" 
                                            data-dismiss="alert">×</button>`;
                                            
                            var header = document.createElement("strong");
                            header.className = "text-capitalize";
                            var title = document.createTextNode(responseDict[key]['title']);

                            var body = document.createElement("p");
                            body.style.marginBottom = "0";
                            var description = document.createTextNode(makeSentenceCase(responseDict[key]['description']));

                            var footer = document.createElement("small");
                            var time = document.createTextNode(parseDateTime(responseDict[key]['time']));

                            link.appendChild(div);
                            div.appendChild(header);
                            header.appendChild(title);
                            div.appendChild(body);
                            body.appendChild(description);
                            div.appendChild(footer);
                            footer.appendChild(time);

                            nContainer.appendChild(link);
                            link.onclick = function() {markAsRead(String(key));};
                        }
                    }
                }
            }
        }
    };
    xhr.send();
}


function markAsRead(pk=""){
    var xhr = new XMLHttpRequest();
    if (pk === "") {
        var url = myapp.URLS.notificationsAllRead; 
    }
    else {
        var url = getAbsoluteURL(`/notifications/${pk}/nread/`);
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
}


function deleteNotifications(pk=""){
    var xhr = new XMLHttpRequest();
    if (pk === "") {
        var url = myapp.URLS.notificationsAllClear;
    }
    else {
        var url = getAbsoluteURL(`/notifications/${pk}/nremove/`);
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
}


function parseDateTime(isoFormat) {
    date = new Date(isoFormat);
    return date.toDateString() + " at " + date.toLocaleTimeString().substr(0, 5);
}


function getAbsoluteURL(path){
    return window.location.protocol + "//" + window.location.host + path;
}


const makeSentenceCase = (s) => {
    if (typeof s !== 'string') return ''
    return s.charAt(0).toUpperCase() + s.slice(1);
}


$("#notificationsDropdown").on("show.bs.dropdown", function() {
    getNotifications();
    getUnreadCount();
});


$('.dropdown').on('show.bs.dropdown', function() {
    $(this).find('.dropdown-menu').first().stop(true, true).slideDown(100);
});


$('.dropdown').on('hide.bs.dropdown', function() {
    $(this).find('.dropdown-menu').first().stop(true, true).slideUp(100);
});


window.setInterval(getUnreadCount, 30000);
