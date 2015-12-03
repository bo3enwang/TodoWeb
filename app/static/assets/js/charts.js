/**
 * Created by Zovven on 2015/12/3.
 */
var lineChartMaker = (function () {
    var _option;
    var todoChart = function () {
        postData();
        _option = {
            title: {
                text: '今日待办完成用时',
                subtext: '总用时',
                x: 'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                x: 'left',
                data: ['计划', '紧急', '优先', '普通']
            },
            toolbox: {
                show: true,
                feature: {
                    mark: {show: true},
                    dataView: {show: true, readOnly: false},
                    magicType: {
                        show: true,
                        type: ['pie', 'funnel'],
                        option: {
                            funnel: {
                                x: '25%',
                                width: '50%',
                                funnelAlign: 'left',
                                max: 1548
                            }
                        }
                    },
                    restore: {show: true},
                    saveAsImage: {show: true}
                }
            },
            calculable: true,
            series: [
                {
                    name: '待办完成情况',
                    type: 'pie',
                    radius: '55%',
                    center: ['50%', '60%'],
                    data: []
                }
            ]
        };
        $.ajax({
            type: 'post',
            contentType: "application/json; charset=UTF-8",
            url: '/admin/todo/chart/pie',
            dataType: 'json',
            data: JSON.stringify({
                'start_date': "2015-01-01",
                'end_date': "2015-12-01"
            }),
            error: function (xhr, err) {
                $.globalMessenger().post({
                    message: '请求数据失败,请重试!',
                    type: 'info',
                    showCloseButton: true
                });
            },
            success: function (data, textStatus) {
                _option.series[0].data = data.result;
            }
        });
        return _option;
    };

    function postData() {

    }

    return {
        todoChart: todoChart
    };
})();