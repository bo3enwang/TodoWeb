/**
 * Created by Zovven on 2015/8/10.
 */
(function ($) {

    $(document).ready(function () {
        fullWidthHeight();
    });

    $(window).resize(function () {
        fullWidthHeight();
    });

    function fullWidthHeight() {
        var w = $(window).width();
        var h = $(window).height();
        $(".time-main").css({
            "min-height": h*0.9
        });
    }
})(jQuery);

function type_normal() {
    $("#type").val(1);
    $("#typeName").html("普通");
}

function type_first() {
    $("#type").val(5);
    $("#typeName").html("优先");
}

function addproject_submit() {
    $("#addproject_form").submit();
}

