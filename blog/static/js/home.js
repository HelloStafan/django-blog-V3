
$(function () {

    // 将首页的banner设为全屏
    var screenHeight = window.innerHeight;
    $(".banner").height(screenHeight);

    // 将首页一开始设为无法滚动（只有这个有关闭这两个属性的方法，所以在这里设置）
    $("body").css("overflow","hidden");
    $("body").css("position","fixed");


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
        $("body").css("position","static");
        $("html").animate({scrollTop:0});

        // 2020/1/1 补充
        // 4. 背景色还原
        $(".navbar").removeClass("navbar-light");
        $(".navbar").addClass("navbar-dark");
    })
        
    

  
    // 点击首页   还是直接刷新吧...


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
    // 不行，还是会清空，因为浏览器刷新，整个文档都清空了
    // ↓
    // 解决:  见本文件最上面
})