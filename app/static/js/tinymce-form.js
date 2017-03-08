//scripts related to forms with the TinyMCE widget

var confirmExit = function (e)
{
    e = e || window.event;
    var message = 'Are you sure you want to leave this page? Any changes you have made will not be saved.';

    if (e)
    {
        e.returnValue = message;
    }

    return message;
};
window.onbeforeunload = confirmExit;

function doSubmit() {
	  window.onbeforeunload = null;
    document.getElementById("bodyhtml").value = tinymce.get('editor').getContent();
    document.forms[0].submit();
}
