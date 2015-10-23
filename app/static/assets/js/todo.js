/**
 * Created by Zovven on 2015/9/2.
 */

function ajaxDataTodo(t_date) {
    if (t_date == null) {
        t_date = moment().format("YYYY-MM-DD");
    }
    $("#todo-date").text(t_date);
    $("#t_date").val(t_date);
    $.ajax({
        type: 'post',
        contentType: "application/json; charset=UTF-8",
        url: '/admin/todo/p/data',
        dataType: 'json',
        data: JSON.stringify({
            't_date': t_date
        }),
        error: function (xhr, err) {
            alert('请求失败，原因可能是：' + err + '！')
        },
        success: function (data, textStatus) {
            var json = $.parseJSON(data.result);
            $("#todo-list").empty();
            $.each(json, function () {
                var li = $("#ul_template_todo li").clone();
                li.find(".cell-checkbox").val(this.id);
                if (this.status == 1) {
                    li.addClass("done");
                    li.find(".cell-checkbox").attr("checked", "checked");
                }
                li.find(".cell-delete").attr("data-id",this.id);
                li.find(".cell-name").text(this.name);
                $("#todo-list").append(li);
            });
            addFuntion();
        }
    });
}


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
            message: '任务名不正确',
            validators: {
                notEmpty: {
                    message: '任务名不能为空'
                },
                stringLength: {
                    min: 1,
                    max: 30,
                    message: '任务不能超过30个字符'
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
            var date = $("#todo-date").text();
            ajaxDataTodo(date);
        }
    }, 'json');
});

function addFuntion() {
    $('.todo-list input[type=checkbox]').on('change', function () {
        var ele = $(this).parents("li").first();
        ele.toggleClass("done");
        id = ele.find();
        if ($('input', ele).is(":checked")) {
            ajaxChange($(this).val(), 1);
        } else {
            ajaxChange($(this).val(), 0);
        }
    });

    $(".cell-delete").confirm({
        text: "确定要删除任务吗?",
        title: "删除任务",
        confirm: function (button) {
            id = button.attr("data-id");
            $.ajax({
                type: 'post',
                contentType: "application/json; charset=UTF-8",
                url: '/admin/todo/delete',
                dataType: 'json',
                data: JSON.stringify({
                    'id': id
                }),
                error: function (xhr, err) {
                    alert('请求错误' + err + '原因')
                },
                success: function (data, textStatus) {
                    if (data.result > 0) {
                        var date = $("#todo-date").text();
                        ajaxDataTodo(date);
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

function ajaxChange(id, status) {
    $.ajax({
        type: 'post',
        contentType: "application/json; charset=UTF-8",
        url: '/admin/todo/change',
        dataType: 'json',
        data: JSON.stringify({
            'id': id,
            'status': status
        }),
        error: function (xhr, err) {
            alert('请求失败，原因可能是：' + err + '！')
        },
        success: function (data, textStatus) {
            if (data.result <= 0) {
                $.globalMessenger().post({
                    message: '更改状态失败',
                    type: 'info',
                    showCloseButton: true
                });
            }
        }
    });
}
function nextDay() {
    var date = $("#todo-date").text();
    day = moment(date);
    day.add(1, 'd');
    ajaxDataTodo(day.format("YYYY-MM-DD"));
}
function lastDay() {
    var date = $("#todo-date").text();
    day = moment(date);
    day.add(-1, 'd');
    ajaxDataTodo(day.format("YYYY-MM-DD"));
}