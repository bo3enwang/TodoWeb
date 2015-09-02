/**
 * Created by Zovven on 2015/9/1.
 */
$(document).ready(function () {
    //�ƻ���ӱ���֤
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
                        message: '�ƻ�������Ϊ��'
                    },
                    stringLength: {
                        min: 1,
                        max: 30,
                        message: '�ƻ���������1��30���ַ�֮��'
                    }
                }
            },
            p_all: {
                validators: {
                    notEmpty: {
                        message: '�ƻ����Ȳ���Ϊ��'
                    },
                    lessThan: {
                        value: 3000,
                        inclusive: true,
                        message: '���Ȳ��ܴ���3000'
                    },
                    greaterThan: {
                        value: 100,
                        inclusive: true,
                        message: '���Ȳ���С��100'
                    }
                }
            },
            p_day: {
                validators: {
                    notEmpty: {
                        message: '�ƻ���������Ϊ��'
                    },
                    lessThan: {
                        value: 999,
                        inclusive: true,
                        message: '�������ܴ���999'
                    },
                    greaterThan: {
                        value: 7,
                        inclusive: true,
                        message: '��������С��7'
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
                $.globalMessenger().post("�����ɹ�!");
                $('#form_project_add').data('bootstrapValidator').resetForm(true);
                $('#modal_project_add').modal('hide')
            }
        }, 'json');
    });

    //�ƻ���¼����֤
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
                alert('����ʧ�ܣ�ԭ������ǣ�' + err + '��')
            },
            success: function (data, textStatus) {
                if (data.result > 0) {
                    $.globalMessenger().post("��¼�ɹ�!");
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
    modal.find('.modal-body #proid').val(proid);//��Ӽƻ�id��������
    $('#form_project_record').bootstrapValidator('addField', 'record', {//��̬�����֤
        message: '����д��ȷ�������',
        validators: {
            notEmpty: {
                message: '���������Ϊ��'
            },
            lessThan: {
                value: remain,
                inclusive: true,
                message: '��������ܴ���' + remain
            },
            greaterThan: {
                value: 1,
                inclusive: true,
                message: '���������С��1'
            }
        }
    });
});

$(".begin").confirm({
    text: "��ȷ��Ҫ����ƻ�",
    title: "����?",
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
                alert('����ʧ�ܣ�ԭ������ǣ�' + err + '��')
            },
            success: function (data, textStatus) {
                if (data.result > 0) {
                    tr.remove();
                    $.globalMessenger().post("����ɹ�!");
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
