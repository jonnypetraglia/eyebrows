$(window).load(function() {
    $(function($) {
        $(".swipebox").swipebox();
    });

    $(".img-file").click(function(event) {
        event.preventDefault();
        var val = $(this).text();
        clickImage(val)
        event.stopPropagation();
    });
    $("#select-all").click(function() {
        $('.chk').prop('checked', $(this).prop('checked'));
        updateDownloadCount();
    });

    $(".chk").click(function(event) {
        updateDownloadCount();
        event.stopPropagation();
    });

    $("#dl-button").click(downloadChecked);

    updateDownloadCount();
    
    
    $('body').click(function(e) {
        $('[data-toggle="popover"]').each(function () {
            //the 'is' for buttons that trigger popups
            //the 'has' for icons within a button that triggers a popup
            if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
                $(this).popover('hide');
            }
        });
    });


    $(".clickableRow").click(function(event) {
        var icon = $($($(this).children()[1]).children()[0]);
        var href = $($($(this).children()[2]).children()[0]);
        console.log(href);
        if(icon.hasClass("fa-picture-o"))
        {

            clickImage(href.text());
            event.preventDefault();
        } else {
            window.document.location = href.attr("href");
        }
    });

    try {$('tbody.rowlink').rowlink(); } catch(e) {}
});

function updateDownloadCount() {
    var c = $("input:checkbox:checked.chk").length;
    switch(c) {
        case 0:
            $("#dl-button").parent().hide();
            break;
        case 1:
            $("#dl-button").parent().show();
            $("#dl-button").text(c + " item");
            break;
        default:
            $("#dl-button").parent().show();
            $("#dl-button").text(c + " items");
    }
}

function downloadChecked() {
    $("input:checkbox:checked.chk").each(function(){
        console.log($(this).val());
    });
}


function clickImage(val) {
    var i;
    for(i = 0; i<window.imageArray.length; i++) {
        if(window.imageArray[i].title == val)
            break;
    }
    $.swipebox(window.imageArray, {initialIndexOnArray: i, hideBarsDelay : hideBarsDelay});
    console.log("Clicked image" + i);
}