$(document).ready(function()
{
    $('#panelForm').on('submit', function(e)
    {
        e.preventDefault()
    });
    $('#panelForm button[type=submit]').on('click', function()
    {
        $.post('/usePanel',{value: $(this).val()});
    });
});
