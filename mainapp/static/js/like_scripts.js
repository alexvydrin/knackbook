window.onload = function () {

    $('.like-article').on('click', '.like-articles', function () {
        let pk = $(this).attr('data-pk');
        if (pk) {
            $.ajax({
                url:"/likes/like_article/" + pk + "/",

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

    $('.like-user').on('click', '.like-users', function () {
        let pk = $(this).attr('data-pk');
        if (pk) {
            $.ajax({
                url: "/likes/like_user/" + pk + "/",

                success: function (data) {
                    $('.like-users').html(data.result);
                    let text_black = $('.like-user').hasClass('.text-danger')
                    let text_red = $('.like-user').hasClass('text-danger')
                    if (text_black == false) {
                        $('.like-user').addClass('text-danger');
                    }
                    if (text_red) {
                        $('.like-user').removeClass('text-danger');
                    }
                }
            });
        }
        event.preventDefault();
    });

}
