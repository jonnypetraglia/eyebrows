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
});