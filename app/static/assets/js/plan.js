/**
 * Created by Zovven on 2015/12/1.
 */
$(document).ready(function () {
    confirmAdd();
    //计划添加表单验证
    $('#form_plan_add').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            plan_type: {
                validators: {
                    notEmpty: {
                        message: '请选择计划类型'
                    }
                }
            },
            plan_name: {
                message: '计划名不正确',
                validators: {
                    notEmpty: {
                        message: '计划名不能为空'
                    },
                    stringLength: {
                        min: 1,
                        max: 30,
                        message: '计划名不能超过30个字符'
                    }
                }
            },
            plan_total: {
                validators: {
                    notEmpty: {
                        message: '计划总长不能为空'
                    },
                    lessThan: {
                        value: 9999,
                        inclusive: true,
                        message: '计划总长不能超过9999'
                    },
                    greaterThan: {
                        value: 10,
                        inclusive: true,
                        message: '计划总长不能小于10'
                    }
                }
            },
            plan_day: {
                validators: {
                    notEmpty: {
                        message: '计划天数不能为空'
                    },
                    lessThan: {
                        value: 999,
                        inclusive: true,
                        message: '计划天数不能超过999'
                    },
                    greaterThan: {
                        value: 3,
                        inclusive: true,
                        message: '计划天数不能小于3'
                    }
                }
            }
        }
    });
    //计划记录表单验证
    $('#form_plan_record').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {}
    });
    //计划记录模态框动态添加验证和滑动条
    $('#modal_plan_record').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var plan_id = button.data('id'); // Extract info from data-* attributes
        var plan_remain = button.data('remain');
        var plan_total = button.data('total');
        var plan_point = button.data('point');
        var modal = $(this);
        modal.find('.modal-body #plan_id').val(plan_id);//动态更改计划id
        $('#form_plan_record').bootstrapValidator('addField', 'record_point', {//动态添加验证
            message: '请输入正确的记录数',
            validators: {
                notEmpty: {
                    message: '记录数不能为空'
                },
                lessThan: {
                    value: plan_remain,
                    inclusive: true,
                    message: '记录数不能大于' + plan_remain
                },
                greaterThan: {
                    value: 1,
                    inclusive: true,
                    message: '记录数不能小于1'
                }
            }
        });
        recordSliderAdd(plan_point, plan_total, plan_remain);
    });
    var table = $('#dataTable').DataTable({
        "dom": '<"top"f >rt<"bottom"ilp><"clear">',//dom定位
        "dom": 'tiprl',//自定义显示项
        "order": [[4, "asc"]],
        columnDefs: [
            {orderable: false, targets: 0},
            {orderable: false, targets: 1},
            {orderable: false, targets: 3},
            {orderable: false, targets: 5}
        ],
        "searching": true,//本地搜索
        "lengthChange": false//是否允许用户自定义显示数量
    });
    $("#typeSelect").change(function () {
        var typeVar = $(this).children('option:selected').val();//这就是selected的值
        table.column(0).search(typeVar).draw();
    });
});
function recordSliderAdd(plan_point, plan_total, plan_remain) {
    var $range = $("#recordSlider");
    slider = $range.data("ionRangeSlider");
    slider && slider.destroy();
    $range.ionRangeSlider({
        type: "single",
        min: 1,
        max: plan_total,
        from: plan_point + 1,
        from_min: plan_point + 1,
        from_max: plan_total,
        from_shadow: true
    });
    $range.on("change", function () {
        var $this = $(this),
            value = $this.prop("value");
        $("#record_point").val(value - plan_point);
        $('#form_plan_record').bootstrapValidator('revalidateField', 'record_point');
    });

    var slider = $range.data("ionRangeSlider");

    $("#record_point").on('keyup paste', function () {
        var currentVal = Number($(this).val());
        var sliderValue = currentVal + plan_point;
        if (isNaN($(this).val())) {
            sliderValue = plan_point + 1;
            $("#record_point").val(1);
            $('#form_plan_record').bootstrapValidator('revalidateField', 'record_point');
        } else if (currentVal > plan_remain) {
            sliderValue = plan_total;
            $("#record_point").val(plan_remain);
            $('#form_plan_record').bootstrapValidator('revalidateField', 'record_point');
        } else if (currentVal < 1) {
            sliderValue = plan_point + 1;
            $("#record_point").val(1);
            $('#form_plan_record').bootstrapValidator('revalidateField', 'record_point');
        }
        slider.update({
            from: sliderValue
        });
    });
}
function confirmAdd() {
    $(".plan_delete").confirm({
        text: "确定要删除计划?",
        title: "删除计划",
        confirm: function (button) {
            var plan_id = button.attr("data-id");
            $.ajax({
                type: 'post',
                contentType: "application/json; charset=UTF-8",
                url: '/admin/plan/' + plan_id + '/delete/',
                dataType: 'json',
                error: function (xhr, err) {
                    console.log('请求错误' + err + '原因')
                },
                success: function (data, textStatus) {
                    if (data.success) {
                        if (data.redirect_url) {
                            window.location.href = data.redirect_url;
                        } else if (data.reload) {
                            window.location.reload();
                        }
                    } else {
                        $.globalMessenger().post({
                            message: '删除失败',
                            type: 'info',
                            showCloseButton: true
                        });
                    }
                }
            });
        },
        cancel: function (button) {
            // nothing to do
        },
        confirmButton: "确定",
        cancelButton: "取消",
        post: true,
        confirmButtonClass: "btn-danger",
        cancelButtonClass: "btn-default",
        dialogClass: "modal-dialog modal-xs" // Bootstrap classes for large modal
    });
    $(".plan_activation").confirm({
        text: "确定要激活计划?",
        title: "激活计划",
        confirm: function (button) {
            var plan_id = button.attr("data-id");
            $.ajax({
                type: 'post',
                contentType: "application/json; charset=UTF-8",
                url: '/admin/plan/' + plan_id + '/activation/',
                dataType: 'json',
                error: function (xhr, err) {
                    console.log('请求错误' + err + '原因')
                },
                success: function (data, textStatus) {
                    if (data.success) {
                        if (data.redirect_url) {
                            window.location.href = data.redirect_url;
                        } else if (data.reload) {
                            window.location.reload();
                        }
                    } else {
                        $.globalMessenger().post({
                            message: '删除失败',
                            type: 'info',
                            showCloseButton: true
                        });
                    }
                }
            });
        },
        cancel: function (button) {
            // nothing to do
        },
        confirmButton: "确定",
        cancelButton: "取消",
        post: true,
        confirmButtonClass: "btn-danger",
        cancelButtonClass: "btn-default",
        dialogClass: "modal-dialog modal-xs" // Bootstrap classes for large modal
    });
}