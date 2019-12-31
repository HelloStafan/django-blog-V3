// 侧边栏的处理
$(function () {

    // 侧边栏的二级菜单;
    // 获取下拉按钮
    
    var slideBtns = document.getElementsByClassName("slide-btn");
    // 注册点击事件 → 按钮自身更改类名 → 激活
    for (var i = 0; i < slideBtns.length; i++) {
        slideBtns[i].onclick = function () {
            this.classList.toggle("active");
        }
    }

    // 侧边栏点击使 右侧内容偏移;
    var content = $(".sidebar").has("#check").siblings(".content");

    $("#close").click(function () {
        content.css("margin-left", "0px")
    })
    $("#open").click(function () {
        content.css("margin-left", "10%");
    })
})
