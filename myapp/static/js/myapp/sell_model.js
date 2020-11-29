var alert_msg ='<div  class="alert alert-success alert-dismissible fade show  " role="alert" id="buy_success">'+
                 'Process has been successfully completed.'+
                 '<button type="button" class="close" data-dismiss="alert" aria-label="Close">'+
                 '<span aria-hidden="true">&times;</span></button></div>';

function getSellForm(counter) {
    $('#sellModel'+counter).modal('show');

}


function updateSellStockTable(){

            $.ajax({
            method: "GET",
            url: '',
            success: function(data) {
                $('#bought-stocks-table').replaceWith($('#bought-stocks-table',data));
            },
            error: function(data) {
                console.log("error")
            }
    })
}


function submitvalidate(id){

    $('#sellForm'+id).submit(function(e){
    path = '../../stock/'+Number(id)+'/sell/';
    console.log('path = '+path);
    $.post(path, $(this).serialize(), function(data){
        //$('.message').html(data.message);
        document.getElementById('alert').innerHTML = alert_msg;
        $('.sellModel').modal('hide');
        updateSellStockTable();

    });
    e.preventDefault();


});
}
function multiply(id){
    gainLoss = Number(document.getElementById('gainLoss'+id).value);
    qty = Number(document.getElementById('quantity'+id).value);
    price = Number(document.getElementById('staticPrice'+id).value);
    document.getElementById('staticTotal'+id).value = Math.round(qty * price * 100) / 100;
    document.getElementById('netGainLoss'+id).value = Math.round(qty * gainLoss * 100) / 100;
}