/**
 * Created by Zovven on 2015/8/10.
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
        $(".time-main").css({
            width: w,
            "min-height": h
        });
    }
})(jQuery);
