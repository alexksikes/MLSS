function highlight_row(e) {
    ele = e.parentNode.parentNode;
    color = ele.style.backgroundColor;
    if (e.checked) {
        color = '#FBFFBF';
    }
    else {
        color = '';
    }
    ele.style.backgroundColor = color;
}

function replace_elm(id, by_id) {
    var elm = document.getElementById(id);
    if (elm) { elm.style.display = 'none'; }
    elm = document.getElementById(by_id);
    if (elm) { elm.style.display = 'block'; }
}

function TB_init(){
    $("form.thickbox").submit(function(){
    var t = this.title || this.name || null;
    var g = this.rel || false;
    TB_show(t,this.action,g);
    this.blur();
    return true;
    });

    $("a.thickbox").click(function(event){
    // stop default behaviour
    event.preventDefault();
    // remove click border
    this.blur();

    // get caption: either title or name attribute
    var caption = this.title || this.name || "";

    // get rel attribute for image groups
    var group = this.rel || false;

    // display the box for the elements href
    TB_show(caption, this.href, group);
    });
}

/*
$("form.thickbox").submit(function(){
    var t = this.title || this.name || null;
    var g = this.rel || false;
    TB_show(t,this.action,g);
    this.blur();
    return true;
});*/