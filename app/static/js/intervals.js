setInterval( function()
{
    $("#volume").load(location.href+" #volume>*","");

    $("#stateButton").load(location.href+" #stateButton>*","");
    $("#current").load(location.href+" #current>*","");
    $("#next").load(location.href+" #next>*","");
},1000);
