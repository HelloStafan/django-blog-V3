

$(function () {
    var beforePos = 0;

    $(window).scroll(function () {
        var nowPos = $(window).scrollTop();
        console.log(nowPos)
        if (nowPos > beforePos) {
            $(".navbar").addClass("navbar-slide-up");
        } else {
            $(".navbar").removeClass("navbar-slide-up");
        }
        beforePos = nowPos;
    })

})