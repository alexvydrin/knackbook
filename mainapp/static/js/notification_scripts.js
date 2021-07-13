window.onload = function () {

    $('.edit-button').on('click', '.edit-buttons', function () {
        let pk = $(this).attr('data-pk');
        if (pk) {
            $.ajax({
                url: "/notification/notification_edit/" + pk + "/",

                success: function (data) {
                    document.getElementById(pk).value = 'Прочитано'
                    document.getElementById(pk).classList.remove('btn-info')
                    document.getElementById(pk).classList.add('btn-success')
                }
            })
        }
    })
    event.preventDefault();

    $('.delete-button').on('click', '.delete-buttons', function () {
        let pk = $(this).attr('data-pk');
        if (pk) {
            $.ajax({
                url: "/notification/notification_delete/" + pk + "/",

                success: function (data) {
                    document.getElementById('n' + pk).remove()
                }
            })
        }
    })
}
