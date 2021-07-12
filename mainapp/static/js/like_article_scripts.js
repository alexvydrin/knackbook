window.onload = function () {

    $('.like-article').on('click', '.like-articles', function () {
        let pk = $(this).attr('data-pk');
        if (pk) {
            $.ajax({
                url:"/likes/like/" + pk + "/",

                success: function(data) {
                    $('.like-articles').html(data.result);
                    let text_black = $('.like-article').hasClass('.text-danger')
                    let text_red = $('.like-article').hasClass('text-danger')
                    if (text_black == false) {
                        $('.like-article').addClass('text-danger');
                    }
                    if (text_red) {
                        $('.like-article').removeClass('text-danger');
                    }
                }
            });
        }
        event.preventDefault();
    });

}
