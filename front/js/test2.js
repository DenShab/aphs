var TRange=null;

function findString (str) {
    if (parseInt(navigator.appVersion)<4) return;
    var strFound;
    if (window.find) {

        // CODE FOR BROWSERS THAT SUPPORT window.find
        strFound=self.find(str);
        if (!strFound) {
            strFound=self.find(str,0,1);
            while (self.find(str,0,1)) continue;
        }
    }
    else if (navigator.appName.indexOf("Microsoft")!=-1) {

        // EXPLORER-SPECIFIC CODE

        if (TRange!=null) {
            TRange.collapse(false);
            strFound=TRange.findText(str);
            if (strFound) TRange.select();
        }
        if (TRange==null || strFound==0) {
            TRange=self.document.body.createTextRange();
            strFound=TRange.findText(str);
            if (strFound) TRange.select();
        }
    }
    else if (navigator.appName=="Opera") {
        $('#srchform2').hide();
        alert ("Il browser opera non è supportato")
        return;
    }
    if (!strFound) alert ("testo non trovato!")
    return;
}

 $(document).on('click', '.searchButtonClickText_h', function (event) {
findString($('.textSearchvalue_h').val());

    });


async function getDoc() {
    var id = localStorage['id'];
    console.log(id);
    localStorage.removeItem( 'id' ); // Clear the localStorage
    var firstData = id;
    await eel.get_doc_adapter(firstData)(callBack);

}

function getForm() {
    console.log('getForm');
    var output =document.querySelector('#doc').innerHTML;
    var iframe = document.getElementsByClassName('ke-edit-iframe')[0];
    var iframeDocument = iframe.contentDocument ;

    iframeDocument.getElementsByClassName('ke-content')[0].innerHTML = output;
    document.getElementsByClassName('ke-edit')[0].removeAttribute('style');
    iframe.removeAttribute('style');
    document.getElementsByClassName('ke-edit')[0].setAttribute('id','root');


}

function callBack(output){
    console.log("callBack");
    console.log(output);
    document.querySelector('#doc').innerHTML = output;
    var searchTerm = localStorage['searchTerm'];
        console.log(searchTerm);

    //searchAndHighlight(searchTerm);
    //doSearch(searchTerm)
        console.log('searchTerm');
        console.log(searchTerm);
        $('.textSearchvalue_h').val(searchTerm);
    findString(searchTerm);
   
}

function get_selected_text() {
    var output =document.querySelector('#doc').innerHTML;
    var iframe = document.getElementsByClassName('ke-edit-iframe')[0];
    var iframeDocument = iframe.contentDocument ;

	if (iframeDocument.getSelection()) {
		var select = iframeDocument.getSelection();
		alert(select.toString());
	}
}



async function openDoc(target,id) {
    if (document.querySelector('#form_editor').classList.contains('d-none')){
        $('#form_editor').removeClass('d-none');
        getForm();
        $('#form_reader').addClass('d-none');
        getForm();
    }
    else {
        $('#form_editor').addClass('d-none');
        $('#form_reader').removeClass('d-none');
    }



}




function doSearch(text) {
    if (window.find && window.getSelection) {
        document.designMode = "on";
        var sel = window.getSelection();
        sel.collapse(document.body, 0);

        while (window.find(text)) {
            document.execCommand("HiliteColor", false, "yellow");
            sel.collapseToEnd();
        }
        document.designMode = "off";
    } else if (document.body.createTextRange) {
        var textRange = document.body.createTextRange();
        while (textRange.findText(text)) {
            textRange.execCommand("BackColor", false, "yellow");
            textRange.collapse(false);
        }
    }
}