$(function() {

	// 获取按钮
	// var pager = document.getElementsByClassName('pager')[0]
	var inputBtn = document.getElementById('btn')
	var previousBtn = document.getElementById('previous')
	var nextBtn = document.getElementById('next')

	// 加载loading效果
	function loading() {
		var html = '<img src="/static/img/loading.gif" />'
        $(".post-list").html(html);
	}	
	// 根据参数：现在页，更新 前/现在/后 3个按钮的值
	function updateBtn(nowPage) {
		var nowpage =  parseInt(nowPage)
		var pre = nowpage - 1
		var next = nowpage + 1
		inputBtn.value = nowpage
		previousBtn.value =  pre
		nextBtn.value =  next
	}
	// 
	function ajaxEvent() {
		// 获取当前调用该方法的对象的value
		var page = this.value

		if (page > 0) {
			$(window).scrollTop(0)
			loading()
			updateBtn(page)

    		// 伪loading效果
    		var queryParas = getParas(page)
    		setTimeout(function () {
		        getPostByAjax(queryParas)
		    }, 600);
		}
	}

	// ajax事件绑定
	inputBtn.onchange = ajaxEvent
	previousBtn.onclick = ajaxEvent
	nextBtn.onclick = ajaxEvent

	// 获取ajax请求的相关参数 
	function getParas(page) {
		var requestList = window.location.pathname.split('/')
		var queryParas = {}
		queryParas.page = page
		if (requestList[2] == 'tag') {
			queryParas.tag = requestList[3]
		}else if(requestList[2] == 'time') {
			queryParas.year = requestList[3]
			queryParas.month = requestList[4]
		}
		return queryParas
	}	
	
	// ajax请求
	function getPostByAjax(queryParas) {

		$.ajax({
            url: '/blog/getPost?page=' + queryParas.page + "&year=" + queryParas.year + "&month="+ queryParas.month + "&tag=" + queryParas.tag,
            type:'get',

            async: true, 
            beforeSend : function(){
            },
            success : function(data) {    
            	var contentArea = document.getElementsByClassName('post-list')[0]
 
            	if (data == '[]') {
            		contentArea.innerHTML = "<p>暂无更多文章</p>"
            	}else{
            		// 将json数据转化为js对象
					var posts = JSON.parse(data)
					// 调用方法，构造DOM
					var post_list_html =  generate_post_list_html(posts)
					// 填充DOM
					contentArea.innerHTML = post_list_html
            	}
            },
    	});
	} 

	// 生成DOM
	function generate_post_list_html(posts) {

		var post_list = '';

    	for (var post of posts) {

	        // 从每条信息中获取相应的信息
	        title = post['title'];
	        subTitle = post['subTitle'];
	        publish = post['publish'];
	        url = post['url'];
	        tags = post['tags'];

	        post_list += '<div class="panel-info">';
	        // 1.标题 
	        post_list += `	
				<div class="header" >
					<div class="icon left">
							<img src="/static/img/ico.gif">
					</div>
					<h2 class="title">  
						<a href="${ url }">
							${ title }
						</a>
					</h2>
					<div class="sub-title">
						${ subTitle }
					</div>
				</div>
			`
			// 2.脚注
			post_list += `	
				<div class="footer">
					<div class="time"> 
						<i class="iconfont icon-shijian2"></i>
							${ publish }
					</div>
					<div class="tags">
						<i class="iconfont icon-tag"></i>
			`
			for (var tag of tags) {
				post_list += `
					<a href="#"> ${ tag } </a>

				`
			} 
				
			post_list += `
				</div>
				</div>
				</div>
			`	     
	    }
	    return post_list
	}


})
	
