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
            name: {
                message: 'The username is not valid',
                validators: {
                    notEmpty: {
                        message: '计划名不能为空'
                    },
                    stringLength: {
                        min: 1,
                        max: 30,
                        message: '计划名必须在1到30个字符之内'
                    }
                }
            },
            p_all: {
                validators: {
                    notEmpty: {
                        message: '计划长度不能为空'
                    },
                    lessThan: {
                        value: 3000,
                        inclusive: true,
                        message: '长度不能大于3000'
                    },
                    greaterThan: {
                        value: 100,
                        inclusive: true,
                        message: '长度不能小于100'
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
                        message: '天数不能大于999'
                    },
                    greaterThan: {
                        value: 7,
                        inclusive: true,
                        message: '天数不能小于7'
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
                $.globalMessenger().post("新增成功!");
                $('#form_project_add').data('bootstrapValidator').resetForm(true);
                $('#modal_project_add').modal('hide')
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
                alert('请求失败，原因可能是：' + err + '！')
            },
            success: function (data, textStatus) {
                if (data.result > 0) {
                    $.globalMessenger().post("记录成功!");
                    $('#modal_project_record').modal('hide');
                    $('#form_project_record').data('bootstrapValidator').resetForm(true);
                    $('#contactForm').bootstrapValidator('removeField', 'record');
                }
            }
        });
    });
});

$('#modal_project_record').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var proid = button.data('proid'); // Extract info from data-* attributes
    var remain = button.data('remain');
    var modal = $(this);
    modal.find('.modal-body #proid').val(proid);//添加计划id到隐藏域
    $('#form_project_record').bootstrapValidator('addField', 'record', {//动态添加验证
        message: '请填写正确的完成数',
        validators: {
            notEmpty: {
                message: '完成数不能为空'
            },
            lessThan: {
                value: remain,
                inclusive: true,
                message: '完成数不能大于' + remain
            },
            greaterThan: {
                value: 1,
                inclusive: true,
                message: '完成数不能小于1'
            }
        }
    });
});

$(".begin").confirm({
    text: "你确定要激活计划",
    title: "激活?",
    confirm: function (button) {
        tr = button.parent().parent();
        proid = button.attr("proid");
        $.ajax({
            type: 'post',
            contentType: "application/json; charset=UTF-8",
            url: '/project/begin',
            dataType: 'json',
            data: JSON.stringify({
                'proid': proid,
            }),
            error: function (xhr, err) {
                alert('请求失败，原因可能是：' + err + '！')
            },
            success: function (data, textStatus) {
                if (data.result > 0) {
                    tr.remove();
                    $.globalMessenger().post("激活成功!");
                }
            }
        });
    },
    cancel: function (button) {
        // nothing to do
    },
    confirmButton: "Yes I am",
    cancelButton: "No",
    post: true,
    confirmButtonClass: "btn-danger",
    cancelButtonClass: "btn-default",
    dialogClass: "modal-dialog modal-xs" // Bootstrap classes for large modal
});
