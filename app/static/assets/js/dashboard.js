/**
 * Created by Zovven on 2015/12/3.
 */
// 基于准备好的dom，初始化echarts图表
var todoChart = echarts.init(document.getElementById('todo_wrap'));
todo_option = {
    title: {
        text: '今日已经完成待办事项',
        subtext: '总用时',
        x: 'center'
    },
    tooltip: {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} min ({d}%)"
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
            name: '完成用时',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: []
        }
    ]
};
todo_option.series[0].data = getAjaxData(moment().format("YYYY-MM-DD"),moment().format("YYYY-MM-DD"));
todoChart.setOption(todo_option);