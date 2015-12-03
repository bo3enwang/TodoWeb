option = {
    title: {
        text: '动态数据',
        subtext: '纯属虚构'
    },
    tooltip: {
        trigger: 'item'
    },
    legend: {
        data: ['随机数据1', '随机数据2', '随机数据3', '随机数据4', '随机数据5']
    },
    toolbox: {
        show: true,
        feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    polar: [
        {
            indicator: [
                {text: '指标一'},
                {text: '指标二'},
                {text: '指标三'},
                {text: '指标四'},
                {text: '指标五'}
            ],
            center: [document.getElementById('main').offsetWidth - 250, 225],
            radius: 100
        }
    ],
    calculable: false,
    series: [
        {
            name: 'pie',
            type: 'pie',
            radius: [0, 110],
            center: [250, 225],
            data: (function () {
                var res = [];
                var len = 0;
                while (len++ < 5) {
                    res.push({
                        name: '随机数据' + len,
                        value: Math.round(Math.random() * 10)
                    });
                }
                return res;
            })()
        }
    ]
};
var lastIndex = 5;
var axisData;
clearInterval(timeTicket);
timeTicket = setInterval(function () {
    lastIndex += 1;
    // 动态数据接口 addData
    myChart.addData([
        [
            0,        // 系列索引
            {         // 新增数据
                name: '随机数据' + lastIndex,
                value: Math.round(Math.random() * 10)
            },
            false,     // 新增数据是否从队列头部插入
            false,     // 是否增加队列长度，false则自定删除原有数据，队头插入删队尾，队尾插入删队头
            '随机数据' + lastIndex
        ]
    ]);
}, 2000);
                    