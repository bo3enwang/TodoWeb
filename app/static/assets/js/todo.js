/**
 * Created by Zovven on 2015/9/2.
 */
(function ($) {

    $(document).ready(function () {
        fullWidthHeight();

    });

    $(window).resize(function () {
        fullWidthHeight();
    });

    function fullWidthHeight() {
        var h = $(window).height();
        $(".todo-main").css({
            "height": h - 141
        });
    }

})(jQuery);

