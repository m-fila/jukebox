$(document).ready(function()
{
    refreshIndex();
    $('#panelForm button[type=submit]').on('click', function()
    {
        $.post('/usePanel',{value: $(this).val()});
    });
});
function refreshIndex(){
  $.get('/index')
    .done(function(r) {
        var newDom = $(r);
        $('#volume').replaceWith($('#volume',newDom));
        $('#stateButton').replaceWith($('#stateButton',newDom));
        $('#current').replaceWith($('#current',newDom));
        $('#next').replaceWith($('#next',newDom));
     });
  setTimeout(refreshIndex,1000)
};
