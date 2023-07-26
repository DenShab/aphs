window.onload=async function(){
    document.getElementById("searchInput").addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        console.log("searchInput2");
        search();
    }
});

await eel.get_sections_adapter()(set_sections);

}

async function search(){
    console.log("search");
    let text = document.getElementById("searchInput").value;
    let  section = document.getElementById("sections").value;
    let value_cur = await eel.search_adapter(text,section)(call_Back);
        console.log(section);
        console.log(text);
}

async function add(){
    console.log("add");
    let  section = document.getElementById("recipient-name").value;
    console.log(document.getElementById("form").checkValidity());
    modalWindow = document.getElementById("exampleModal");

    if(document.getElementById("form").checkValidity()) {
        $('#exampleModal').modal('hide');
        load();
        console.log(section);
        await eel.add_doc_adapter(section)(hide);
    }
};



function load(){
  $('#myModal').removeClass('d-none');
    $('#main').addClass('d-none')
}

function hide(status){
    console.log(status);
     if (status == 'Ok'){
     $('#myModal').addClass('d-none')
     $('#main').removeClass('d-none');
     window.location.reload();
     }
     else alert('Неправильно.');
}

function set_sections(output){
    console.log("set_sections");
    console.log(output);
    document.querySelector('#sections').innerHTML = "";
    const fragment = document.createDocumentFragment();
        let option = document.createElement('option');
        option.setAttribute("value","%");
        option.textContent = "Все разделы";
        document.querySelector('#sections').appendChild(option);
    output.forEach(function(item) {
        let option = document.createElement('option');
        option.setAttribute("value", item);
        option.textContent = item;
        let option2 = option.cloneNode(true);;
        document.querySelector('#sections').appendChild(option2);
        document.querySelector('#sections_datalist').appendChild(option);
    });
}


function call_Back(output){
    console.log("call_Back");
    document.querySelector('#list-group').innerHTML = "";
    console.log(output);

    output.forEach(function(item) {
        let id = item[0];
        const fragment = document.createDocumentFragment();
        const a = document.createElement('div');

        a.setAttribute("class", "list-group-item list-group-item-action");
        a.setAttribute('onclick', `openDoc("test2.html",${id})`);
        console.log(`newWindow("test2.html",${id})`);
        a.setAttribute("id", id);
        let div = document.createElement('div');
        div.setAttribute("class", "d-flex justify-content-between");
        a.appendChild(div);
        let h5 = document.createElement('h5');
        h5.setAttribute("class", "mb-1");
        h5.textContent = item[1];
        div.appendChild(h5)
        let p = document.createElement('p')
        p.class = 'mb-1';
        p.setAttribute("class", "mb-1");

        p.innerHTML =item[2];
        a.appendChild(p)
        document.querySelector('#list-group').appendChild(a);
    });
}

async function openDoc(target,id  ) {
    localStorage.setItem( 'id', id );
    var node = document.getElementById(id).querySelector('p');
    var searchTerm = node.textContent.replaceAll('...', '').replaceAll('\n',' ');
    let text = document.getElementById("searchInput").value;
    localStorage.setItem( 'searchTerm', text );
    await eel.open_doc_adapter(target)();
}


