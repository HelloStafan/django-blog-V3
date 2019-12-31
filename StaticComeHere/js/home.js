
$(function () {
    
    // 更多
    $(".more").click(function(){

        // 1. 让banner及下的元素全部消失;  
        // height针对盒子，opacity针对内联文字
        $(".banner").find("*").addBack().css("height", "0").css("opacity","0");
        
        // 2. 导航区激活
        $("li.active").has("a#home").removeClass("active");
        $("li").has("a#blog").addClass("active");

        // 3. 滚动恢复正常
        $("body").css("overflow","scroll");
        $("html").animate({scrollTop:0});
    })
        
    
    // 首页   直接刷新吧...

})