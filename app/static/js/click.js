function removeFun(a)
{
    $.post('/removeTrack',{ind: a});
};

function nextAutoFun()
{
    $.post('/nextAuto');
};

