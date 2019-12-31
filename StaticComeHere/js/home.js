
$(function () {
    
    // 更多
    $(".more").click(function() {

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
        
    
    // 点击首页   直接刷新吧...


    // 点击博客  , 滚动恢复正常,,,,恢复不了了。
    //  ↓
    // 这样来恢复正常
    //  ↓
    const scrollAble =  function () {
        $("body").css("overflow","scroll");
    }
    // 点击首页时不自动恢复滚动
    $("#blog").click(function() {
        timer = setTimeout(scrollAble, 600);
        console.log(1)
    })
    // 不行，还是会清空，整个文档都清空了
})