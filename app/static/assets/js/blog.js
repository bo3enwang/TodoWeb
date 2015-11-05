/**
 * Created by Zovven on 2015/11/5.
 */
$(document).ready(function () {
    console.log("What you want?");
    backToTop();
});
/**
 * 回到顶部
 */
function backToTop() {
    var st = $(".page-scrollTop");
    var $window = $("#content");
    var topOffset;
    //滚页面才显示返回顶部
    $window.scroll(function () {
        var currnetTopOffset = $window.scrollTop();
        if (currnetTopOffset > 300 && topOffset > currnetTopOffset) {
            st.fadeIn(500);
        } else {
            st.fadeOut(500);
        }
        topOffset = currnetTopOffset;
    });

    //点击回到顶部
    st.click(function () {
        $window.animate({
            scrollTop: "0"
        }, 500);
    });
}