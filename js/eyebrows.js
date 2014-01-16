$(window).load(function() {
    console.log($(".img-file"));
    $(function($) {
        $(".swipebox").swipebox();
    });

    $(".img-file").click(function(event) {
        event.preventDefault();
        var val = $(this).text();
        var i;
        for(i = 0; i<window.imageArray.length; i++) {
            if(window.imageArray[i].title == val)
                break;
        }
        $.swipebox(window.imageArray, {initialIndexOnArray: i, hideBarsDelay : hideBarsDelay});
        console.log("Clicked image");
    });
    $("#select-all").click(function() {
        $('.chk').prop('checked', $(this).prop('checked'));
        updateDownloadCount();
    });

    $(".chk").click(function() {
        updateDownloadCount();
    });

    $("#dl-button").click(downloadChecked);

    updateDownloadCount();
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
//    with ZipFile('spam.zip', 'w') as myzip:
//    myzip.write('eggs.txt')
}