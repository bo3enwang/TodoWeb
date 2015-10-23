/**
 * Created by Zovven on 2015/9/1.
 */
$(document).ready(function () {
    //计划添加表单验证
    $('#form_project_add').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            type: {
                validators: {
                    notEmpty: {
                        message: '请选择计划类型'
                    }
                }
            },
            name: {
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
            p_all: {
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
            p_day: {
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
    }).on('success.form.bv', function (e) {
        // Prevent form submission
        e.preventDefault();

        // Get the form instance
        var $form = $(e.target);

        // Get the BootstrapValidator instance
        var bv = $form.data('bootstrapValidator');

        // Use Ajax to submit form data
        $.post($form.attr('action'), $form.serialize(), function (result) {
            if (result.result > 0) {
                //Post add success message
                $.globalMessenger().post({
                    message: '添加成功',
                    type: 'info',
                    showCloseButton: true
                });
                $('#form_project_add').data('bootstrapValidator').resetForm(true);
                $('#modal_project_add').modal('hide');
                ajaxDataProject();
            } else {
                $.globalMessenger().post({
                    message: '添加失败',
                    type: 'info',
                    showCloseButton: true
                });
                $('#form_project_add').data('bootstrapValidator').resetForm(true);
                $('#modal_project_add').modal('hide');
            }
        }, 'json');
    });

    //计划记录表单验证
    $('#form_project_record').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {}
    }).on('success.form.bv', function (e) {
        // Prevent form submission
        e.preventDefault();

        // Get the form instance
        var $form = $(e.target);

        // Get the BootstrapValidator instance
        var bv = $form.data('bootstrapValidator');

        // Use Ajax to submit form data
        var record = $("#record").val();
        var proid = $("#proid").val();
        $.ajax({
            type: 'post',
            contentType: "application/json; charset=UTF-8",
            url: $form.attr('action'),
            dataType: 'json',
            data: JSON.stringify({
                'proid': proid,
                'record': record
            }),
            error: function (xhr, err) {
                alert('请求错误' + err + '原因')
            },
            success: function (data, textStatus) {
                if (data.result > 0) {
                    $.globalMessenger().post({
                        message: '记录成功',
                        type: 'info',
                        showCloseButton: true
                    });
                    $('#modal_project_record').modal('hide');
                    $('#form_project_record').data('bootstrapValidator').resetForm(true);
                    $('#contactForm').bootstrapValidator('removeField', 'record');
                    ajaxDataProject();
                } else {
                    $.globalMessenger().post({
                        message: '记录失败',
                        type: 'info',
                        showCloseButton: true
                    });
                    $('#modal_project_record').modal('hide');
                    $('#form_project_record').data('bootstrapValidator').resetForm(true);
                }
            }
        });
    });

    $('#modal_project_record').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var proid = button.data('proid'); // Extract info from data-* attributes
        var remain = button.data('remain');
        var p_all = button.data('all');
        var modal = $(this);
        modal.find('.modal-body #proid').val(proid);//动态更改计划id
        $('#form_project_record').bootstrapValidator('addField', 'record', {//动态添加验证
            message: '请输入正确的记录数',
            validators: {
                notEmpty: {
                    message: '记录数不能为空'
                },
                lessThan: {
                    value: remain,
                    inclusive: true,
                    message: '记录数不能大于' + remain
                },
                greaterThan: {
                    value: 1,
                    inclusive: true,
                    message: '记录数不能小于1'
                }
            }
        });
        recordSliderAdd(p_all, remain);
    });
    confirmAdd();
});

function confirmAdd() {
    $(".p-begin").confirm({
        text: "确定要激活计划?",
        title: "激活计划",
        confirm: function (button) {
            proid = button.attr("proid");
            $.ajax({
                type: 'post',
                contentType: "application/json; charset=UTF-8",
                url: '/admin/project/begin',
                dataType: 'json',
                data: JSON.stringify({
                    'proid': proid,
                }),
                error: function (xhr, err) {
                    alert('请求错误' + err + '原因')
                },
                success: function (data, textStatus) {
                    if (data.result > 0) {
                        ajaxDataProject();
                        $.globalMessenger().post({
                            message: '激活成功',
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

    $(".p-delete").confirm({
        text: "确定要删除计划吗?",
        title: "删除计划",
        confirm: function (button) {
            proid = button.attr("proid");
            $.ajax({
                type: 'post',
                contentType: "application/json; charset=UTF-8",
                url: '/admin/project/delete',
                dataType: 'json',
                data: JSON.stringify({
                    'proid': proid,
                }),
                error: function (xhr, err) {
                    alert('请求错误' + err + '原因')
                },
                success: function (data, textStatus) {
                    if (data.result > 0) {
                        ajaxDataProject();
                        $.globalMessenger().post({
                            message: '删除成功',
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
function recordSliderAdd(p_all, p_remain) {
    var p_now = Number(p_all) - Number(p_remain);
    var $range = $("#record_gra");
    slider = $range.data("ionRangeSlider");
    slider && slider.destroy();
    $range.ionRangeSlider({
        type: "single",
        min: 1,
        max: p_all,
        from: p_now+1,
        from_min: p_now+1,
        from_max: p_all,
        from_shadow: true
    });
    $range.on("change", function () {
        var $this = $(this),
            value = $this.prop("value");
        $("#record").val(value-p_now);
        $('#form_project_record').bootstrapValidator('revalidateField','record');
    });

    var slider = $range.data("ionRangeSlider");

    $("#record").on('keyup paste', function () {
        var currentVal = Number($(this).val());
        var sliderValue = currentVal + p_now;
        if (currentVal > p_remain) {
            sliderValue = p_all;
            $("#record").val(p_remain);
            $('#form_project_record').bootstrapValidator('revalidateField', 'record');
        }else if(currentVal < 1){
            sliderValue = 1;
            $("#record").val(1);
            $('#form_project_record').bootstrapValidator('revalidateField', 'record');
        }
        slider.update({
            from: sliderValue
        });
    });
}