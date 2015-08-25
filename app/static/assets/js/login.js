/**
 * Created by Zovven on 2015/8/25.
 */
/**
 * Created by Zovven on 2015/8/7.
 */
(function ($) {

    $(document).ready(function() {
		fullWidthHeight();

	});

	$(window).resize(function() {
		fullWidthHeight();
	});

    function fullWidthHeight() {
        var w = $(window).width();
        var h = $(window).height();
        $(".index-main").css({
            width: w,
            "min-height": h
        });
    }
})(jQuery);

function toRegister(){

}