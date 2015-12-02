/**
 * Created by Zovven on 2015/9/2.
 */

function addTodoLi(id, todo_status, todo_type, todo_desc, todo_date, todo_time) {
    var typeStr = {};
    typeStr[0] = "计划";
    typeStr[1] = "紧急";
    typeStr[2] = "优先";
    typeStr[3] = "普通";
    var typeCLass = {};
    typeCLass[0] = "label-success";
    typeCLass[1] = "label-danger";
    typeCLass[2] = "label-primary";
    typeCLass[3] = "label-default";

    var appendLocation;
    var li = $("<li></li>");
    var spanType = $("<span></span>", {class: 'label todo-type'});
    var spanDesc = $("<span></span>", {class: 'desc'});
    var spanTime = $("<span></span>", {class: 'time'});
    var spanDate = $("<span></span>", {class: 'date'});
    var spanOperation = $("<span></span>", {class: 'operation pull-right'});
    var btnComplete = $("<button></button>", {class: 'btn btn-default btn-sm'});
    var btnDelete = $("<button></button>", {class: 'btn btn-default btn-sm'});

    spanType.addClass(typeCLass[todo_type]);
    spanType.text(typeStr[todo_type]);
    li.append(spanType);

    spanDesc.text(todo_desc);
    li.append(spanDesc);

    spanDate.text(todo_date);
    li.append(spanDate);

    btnDelete.text("删除");
    btnDelete.confirm({
        text: "确定要删除待办事项?",
        title: "删除待办事项",
        confirm: function (button) {
            $.ajax({
                type: 'post',
                contentType: "application/json; charset=UTF-8",
                url: '/admin/todo/' + id + '/delete/',
                dataType: 'json',
                error: function (xhr, err) {
                    $.globalMessenger().post({
                        message: '删除失败',
                        type: 'info',
                        showCloseButton: true
                    });
                },
                success: function (data, textStatus) {
                    if (data.success) {
                        var operator_li = button.parent().parent();
                        operator_li.slideUp(300, function () {
                            operator_li.remove();
                        });
                        $.globalMessenger().post({
                            message: '删除成功',
                            type: 'info',
                            showCloseButton: true
                        });
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
    spanOperation.append(btnDelete);
    li.append(spanOperation);

    if (todo_status == 1) {
        li.addClass("done");
        appendLocation = $("#todo_completed");
        spanTime.text("完成用时: " + todo_time + " min");
        spanTime.appendTo(li);
    } else {
        appendLocation = $("#todo_none");
        btnComplete.text("完成");
        btnComplete.attr("data-toggle", "modal");
        btnComplete.attr("data-target", "#modal_todo_complete");
        btnComplete.attr("data-id", id);
        btnDelete.before(btnComplete);
    }
    li.css("display", "none");
    li.appendTo(appendLocation);
    li.slideDown(300);
}

function ajaxPostTodoData(start_date, end_date) {
    $.ajax({
        type: 'post',
        contentType: "application/json; charset=UTF-8",
        url: '/admin/todo/json',
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
            if (data.success) {
                $("#todo_none").empty();
                $("#todo_completed").empty();
                $.each(data.result, function () {
                    addTodoLi(this.id, this.todo_status, this.todo_type, this.todo_desc, this.todo_date, this.todo_time);
                });
            } else {
                $.globalMessenger().post({
                    message: '请求数据失败,请重试!',
                    type: 'info',
                    showCloseButton: true
                });
            }
        }
    });
}


function dateToday() {
    var btn_today = $("#btn_today");
    var date_label = $("#date_label");
    btn_today.removeClass("btn-primary");
    btn_today.addClass("btn-primary");
    var today_var = moment().format("YYYY-MM-DD");
    date_label.text(today_var);
    date_label.attr("data-type", "1");
    $("#btn_date_type").find("button").removeClass("btn-primary");
    $("#type_day").addClass("btn-primary");
    ajaxPostTodoData(today_var, today_var);
}
function dateNext() {
    var date_label = $("#date_label");
    var type_var = date_label.attr("data-type");
    var date_text = date_label.text();
    var start_date;
    var end_date;
    var btn_today = $("#btn_today");
    btn_today.removeClass("btn-primary");
    switch (type_var) {
        case '1':
            start_date = moment(date_text).add(1, 'days').format("YYYY-MM-DD");
            var todayMoment = moment().format("YYYY-MM-DD");
            if (moment(todayMoment).isSame(start_date)) {
                btn_today.addClass("btn-primary");
            }
            date_label.text(start_date);
            ajaxPostTodoData(start_date, start_date);
            break;

        case '2':
            start_date = moment(date_text, "YYYY-MM-DD").add(1, 'weeks').format("YYYY-MM-DD");
            end_date = moment(date_text, "YYYY-MM-DD").add(2, 'weeks').format("YYYY-MM-DD");
            date_label.text(start_date + "~" + end_date.substr(end_date.length - 2, 2));
            ajaxPostTodoData(start_date, end_date);
            break;
        case '3':
            start_date = moment(date_text, "YYYY-MM").set('date', 1).add(1, 'month').format("YYYY-MM-DD");
            end_date = moment(date_text, "YYYY-MM").add(2, 'month').subtract(1, 'days').format("YYYY-MM-DD");
            date_label.text(start_date.substr(0, 7));
            ajaxPostTodoData(start_date, end_date);
            break;
    }
}
function datePre() {
    var date_label = $("#date_label");
    var type_var = date_label.attr("data-type");
    var date_text = date_label.text();
    var start_date;
    var end_date;
    var btn_today = $("#btn_today");
    btn_today.removeClass("btn-primary");
    switch (type_var) {
        case '1':
            start_date = moment(date_text).subtract(1, 'days').format("YYYY-MM-DD");
            var todayMoment = moment().format("YYYY-MM-DD");
            if (moment(todayMoment).isSame(start_date)) {
                btn_today.addClass("btn-primary");
            }
            date_label.text(start_date);
            ajaxPostTodoData(start_date, start_date);
            break;

        case '2':
            start_date = moment(date_text, "YYYY-MM-DD").subtract(1, 'weeks').format("YYYY-MM-DD");
            end_date = moment(date_text, "YYYY-MM-DD").subtract(1, 'days').format("YYYY-MM-DD");
            date_label.text(start_date + "~" + end_date.substr(end_date.length - 2, 2));
            ajaxPostTodoData(start_date, end_date);
            break;
        case '3':
            start_date = moment(date_text, "YYYY-MM").subtract(1, 'month').format("YYYY-MM-DD");
            end_date = moment(date_text, "YYYY-MM").subtract(1, 'days').format("YYYY-MM-DD");
            date_label.text(start_date.substr(0, 7));
            ajaxPostTodoData(start_date, end_date);
            break;
    }
}

$(document).ready(function () {
    $("#btn_date_type").find("button").click(function () {
        var btn = $(this);
        var btn_type = btn.attr("data-type");
        var date_label = $("#date_label");
        if (btn_type == date_label.attr("data-type")) {
            return;
        }
        var btn_today = $("#btn_today");
        btn_today.removeClass("btn-primary");
        $("#btn_date_type").find("button").removeClass("btn-primary");

        btn.addClass("btn-primary");
        date_label.attr("data-type", btn_type);
        var start_date;
        var end_date;
        switch (btn_type) {
            case '1':
                btn_today.addClass("btn-primary");
                var today_var = moment().format("YYYY-MM-DD");
                date_label.text(today_var);
                ajaxPostTodoData(today_var, today_var);
                break;
            case '2':
                start_date = moment().startOf('week').format("YYYY-MM-DD");
                end_date = moment().endOf('week').format("YYYY-MM-DD");
                date_label.text(start_date + "~" + end_date.substr(end_date.length - 2, 2));
                ajaxPostTodoData(start_date, end_date);
                break;

            case '3':
                var month_var = moment().format("YYYY-MM");
                start_date = moment().startOf('month').format("YYYY-MM-DD");
                end_date = moment().endOf('month').format("YYYY-MM-DD");
                date_label.text(month_var);
                ajaxPostTodoData(start_date, end_date);
                break;
        }
    });
    $("#date_next").click(function () {
        dateNext();
    });
    $("#date_pre").click(function () {
        datePre();
    });
    $("#btn_today").click(function () {
        dateToday();
    });
    //新增待办添加表单验证
    $('#form_todo_add').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            todo_type: {
                validators: {
                    notEmpty: {
                        message: '请选择计划类型'
                    }
                }
            },
            todo_desc: {
                message: '待办描述不正确',
                validators: {
                    notEmpty: {
                        message: '待办描述不能为空'
                    },
                    stringLength: {
                        min: 1,
                        max: 30,
                        message: '待办描述不能超过30个字符'
                    }
                }
            }
        }
    });
    $('#modal_todo_complete').on('hide.bs.modal', function (e) {
        var operator_li = $("#operator_li");
        if (operator_li != null) {
            operator_li.removeAttr("id");
        }
    });
    //待办完成模态框动态添加Id
    $('#modal_todo_complete').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var modal = $(this);
        modal.find('.modal-body #todo_id').val(button.attr("data-id"));//动态更改计划id
        button.parent().parent().attr("id", "operator_li");
    });
    //待办完成添加表单验证
    $('#form_todo_complete').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            todo_time: {
                validators: {
                    notEmpty: {
                        message: '用时不能为空'
                    },
                    lessThan: {
                        value: 1200,
                        inclusive: true,
                        message: '用时不能大于1200'
                    },
                    greaterThan: {
                        value: 1,
                        inclusive: true,
                        message: '用时不能小于1'
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
        $.post($form.attr('action'), $form.serialize(), function (data) {
            if (data.success) {
                $.globalMessenger().post({
                    message: '待办已经完成',
                    type: 'info',
                    showCloseButton: true
                });
                var operator_li = $("#operator_li");
                operator_li.slideUp(300, function () {
                    operator_li.remove();
                });
                var json_data = data.todo;
                addTodoLi(json_data.id, json_data.todo_status, json_data.todo_type, json_data.todo_desc,
                    json_data.todo_date, json_data.todo_time);
                $('#modal_todo_complete').modal('hide');
                $('#form_todo_complete').data('bootstrapValidator').resetForm(true);
            } else {
                $.globalMessenger().post({
                    message: '设置完成失败',
                    type: 'info',
                    showCloseButton: true
                });
                $('#modal_todo_complete').modal('hide');
                $('#form_todo_complete').data('bootstrapValidator').resetForm(true);
            }
        }, 'json');
    });

    dateToday();
});