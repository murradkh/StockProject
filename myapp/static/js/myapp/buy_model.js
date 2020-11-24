var alert_msg ='<div  class="alert alert-success alert-dismissible fade show  " role="alert" id="buy_success">'+
                 'Process has been successfully completed.'+
                 '<button type="button" class="close" data-dismiss="alert" aria-label="Close">'+
                 '<span aria-hidden="true">&times;</span></button></div>';


function multiply(){
    qty = Number(document.getElementById('quantity').value);
    price = Number(document.getElementById('staticPrice').value);
    document.getElementById('staticTotal').value=Math.round(qty*price * 100) / 100;
}


function  validateForm(){
  var total = Number(document.forms["buyForm"]["Total"].value);
  var budget = Number(document.getElementById('staticBudget').value);
  if (total > budget ) {
    alert("This process is above your budget.");
    return false;
}
return true;
}


function resetForm(){
$("#buyForm")[0].reset();
$('#threshold_div').hide();
}


function isNumberKey(evt, element) {
  var charCode = (evt.which) ? evt.which : event.keyCode
  if (charCode > 31 && (charCode < 48 || charCode > 57) && !(charCode == 46 || charCode == 8))
        return false;
  else {
        var len = $(element).val().length;
        var index = $(element).val().indexOf('.');
        if (index > 0 && charCode == 46) {
              return false;
        }
    if (index > 0) {
      var CharAfterdot = (len + 1) - index;
      if (CharAfterdot > 3) {
        return false;
      }
    }
  }
  return true;
}


$.fn.ShowInput = $(function () {
    $('#threshold_div').hide();
    $('input[name="checkbox"]').on('click', function () {
        if ($(this).prop('checked')) {
            $('#threshold_div').fadeIn();
        } else {
            $('#threshold_div').hide();
        }
    });
});


$(document).ready(function(){
    $('#buy_success').hide();
        $('#buyForm').submit(function(e){
        if (validateForm()){
        $.post('buy/', $(this).serialize(), function(data){
            $('.message').html(data.message);
            document.getElementById('x').innerHTML =alert_msg;
            $('#buyModel').modal('hide');
            resetForm();
        });
        e.preventDefault();
        }
        else{

        return false;
        }
    });
});