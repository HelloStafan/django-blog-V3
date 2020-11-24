$(function() {

	init()

	// 初始化函数 
	function init() {
		var postId = document.getElementById("post-id").value
		var user = document.getElementById("user").value
		
		document.getElementById('thumbs-up-btn').onclick = function() {
			if (!user) {
				alert("点赞请先登录")
				window.location.href = "/user"
			}
			if (this.className == "active") {
				// 发送ajax(取消点赞)
				thumbUp(postId, false)
				this.className = ""
			}else{
				// 发送ajax(点赞)
				thumbUp(postId, true)
				this.className = "active"
			}
			
		}	
		document.getElementById('collect-up-btn').onclick = function() {
			if (!user) {
				alert("收藏请先登录")
				window.location.href = "/user"
			}
			if (this.className == "active") {
				// 发送ajax(取消点赞)
				collect(postId, false)
				this.className = ""
			}else{
				// 发送ajax(点赞)
				collect(postId, true)
				this.className = "active"
			}
		}
	}

	// ajax  点赞
	function thumbUp(postId, flag) {
		$.ajax({
			url: '/blog/thumbUp?flag='+ flag + "&postId=" + postId,
			type: 'get',
			async: true,
			success : function(data) {  
            	var thumbsNumArea = document.getElementById("thumbs-num-area")
            	thumbsNumArea.innerText = JSON.parse(data).now_thumbs + " 赞"
            	}
        	})
	}
	// ajax  收藏
	function collect(postId, flag) {
		$.ajax({
			url: '/blog/collect?flag='+ flag + "&postId=" + postId,
			type: 'get',
			async: true,
			success : function(data) {  
            	var collectNumArea = document.getElementById("collect-num-area")
            	collectNumArea.innerText = JSON.parse(data).now_collects + " 收藏"
            	}
        	})
	}
	
})