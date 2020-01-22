setInterval( function()
{
 $.get('/index')
    .done(function(r) {
        var newDom = $(r);
        $('#volume').replaceWith($('#volume',newDom));
        $('#stateButton').replaceWith($('#stateButton',newDom));
        $('#current').replaceWith($('#current',newDom));
        $('#next').replaceWith($('#next',newDom));
     });
},1000);

