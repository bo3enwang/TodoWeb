/**
 * Created by Zovven on 2015/11/5.
 */
$(document).ready(function () {
    console.log("What you want?");
    backToTop();
});
/**
 * 滑动到顶部
 */
function backToTop() {
    var st = $(".page-scrollTop");
    var $window = $("#content");
    $window.scroll(function () {
        var currnetTopOffset = $window.scrollTop();
        if (currnetTopOffset > 300 ) {
            st.fadeIn(500);
        } else {
            st.fadeOut(500);
        }
    });

    st.click(function () {
        $window.animate({
            scrollTop: "0"
        }, 500);
    });
}