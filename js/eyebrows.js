$(window).load(function() {
    $(function($) {
        $(".swipebox").swipebox();
    });
    
    $(window).on('hashchange', onHashChange);
    
    // Change hash immediately if need be
    if(window.location.hash!="") {
        var sansHash = window.location.href.substr(0, window.location.href.length - window.location.hash.length)
        var hash = window.location.hash.substr(1);
        console.log("ReplaceState", sansHash);
        history.replaceState(null, null, sansHash)
        changeHash(hash);
    }

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
    
    var clickableRows = $(".clickableRow");


    clickableRows.click(function(event) {
        var icon = $($($(this).children()[1]).children()[0]);
        var href = $($($(this).children()[2]).children()[0]);
        console.log(href);
        if(href.hasClass("swipe"))
        {
            changeHash(href.text());
            event.preventDefault();
        } else
            window.location.href = href.attr("href");
    });

    if(clickableRows.length < 50)
        try {$('tbody.rowlink').rowlink(); } catch(e) {}
    
    clickableRows.hover(function(){
            $(this).find('.info').removeClass('invisible');
        }, function(){
            $(this).find('.info').addClass('invisible');
        }
    );
    
    $('.info-btn').click(function(event) {
        console.log(this);
        $(this).parent('.info').find('.dropdown-toggle').dropdown()
        event.preventDefault();
        event.stopPropagation();
    });
    $('.info-popup').click(function(event) {
        event.preventDefault();
        event.stopPropagation();
    });
    $('.force-download').click(function(event) {
        console.log(this);
        console.log("JUST SAY YOU'RE SORRY");
        event.stopPropagation();
    });
    
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

function onHashChange(event) {
    console.log("hashchange", window.location.hash);
    var filename = window.location.hash.substr(1);
    if(filename == "") {
        if($.swipebox.isOpen) {
            $.swipebox.close();
        }
    }
    else
        clickMedia(filename);
    if(event!=null) {
        event.preventDefault();
        event.stopPropagation();
    }
}

function changeHash(to) {
    if(history.pushState) {
        console.log("pushState", "#"+to);
        history.pushState(null, null, "#" + to);
        onHashChange();
    } else
        window.location.hash = to;
}

function clickMedia(val) {
    var i;
    val = decodeURIComponent(val);
    for(i = 0; i<window.swipeboxArray.length; i++) {
        if(window.swipeboxArray[i].title == val)
            break;
    }
    if(i<window.swipeboxArray.length)
        $.swipebox(window.swipeboxArray,{
            initialIndexOnArray: i,
            hideBarsDelay : hideBarsDelay,
            afterClose: function() {
                console.log("Going Back");
                if(history.pushState)
                    history.back();
            }
        });
    console.log("Clicked media " + i);
}
