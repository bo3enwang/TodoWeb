/**
 * Created by Zovven on 2015/11/5.
 */
$(document).ready(function () {
    console.log("What you want?");
    backToTop();
});
/**
 * �ص�����
 */
function backToTop() {
    var st = $(".page-scrollTop");
    var $window = $("#content");
    var topOffset;
    //��ҳ�����ʾ���ض���
    $window.scroll(function () {
        var currnetTopOffset = $window.scrollTop();
        if (currnetTopOffset > 300 && topOffset > currnetTopOffset) {
            st.fadeIn(500);
        } else {
            st.fadeOut(500);
        }
        topOffset = currnetTopOffset;
    });

    //����ص�����
    st.click(function () {
        $window.animate({
            scrollTop: "0"
        }, 500);
    });
}