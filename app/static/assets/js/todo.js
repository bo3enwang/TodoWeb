/**
 * Created by Zovven on 2015/9/2.
 */
$(document).ready(function () {
    //计划添加表单验证
    $('#form_todo_add').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
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
            t_date: {
                validators: {
                    notEmpty: {
                        message: '计划总长不能为空'
                    },
                    lessThan: {
                        value: 3000,
                        inclusive: true,
                        message: '计划总长不能超过3000'
                    },
                    greaterThan: {
                        value: 100,
                        inclusive: true,
                        message: '计划总长不能小于100'
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
                $('#form_todo_add').data('bootstrapValidator').resetForm(true);
                $('#modal_todo_add').modal('hide');
                ajaxDataTodo();
            }
        }, 'json');
    });
});