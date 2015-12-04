/**
 * Created by Zovven on 2015/12/3.
 */
function getAjaxData(start_date,end_date) {
    var json_data;
    $.ajax({
        type: 'post',
        contentType: "application/json; charset=UTF-8",
        async : false,
        url: '/admin/todo/chart/pie',
        dataType: 'json',
        data: JSON.stringify({
            'start_date': start_date,
            'end_date': end_date
        }),
        error: function (xhr, err) {
            $.globalMessenger().post({
                message: '请求数据失败,请重试!',
                type: 'info',
                showCloseButton: true
            });
        },
        success: function (data, textStatus) {
            json_data= data.result;
        }
    });
    return json_data;
}