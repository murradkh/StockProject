 $(document).ready(function(){
                 var checked = JSON.parse(localStorage.getItem('customSwitch1'));
                 document.getElementById("customSwitch1").checked = checked;
                 document.getElementById("timer").innerHTML =new Date().toLocaleString();
            });
  function handleClick() {
         var checkbox = document.getElementById('customSwitch1');
         localStorage.setItem('customSwitch1', checkbox.checked);
    }