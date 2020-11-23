$(function() {

	init()

	// 初始化函数 
	function init() {
		var postId = document.getElementById("post-id").value
		
		document.getElementById('thumbs-up-btn').onclick = function() {
			if (this.classList.contains("active")) {
				// 发送ajax(取消点赞)
				thumbUp(postId, false)
				this.classList.remove("active")
			}else{
				// 发送ajax(点赞)
				thumbUp(postId, true)
				this.classList.add("active")
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
            	thumbsNumArea.innerText = JSON.parse(data).now_thumbs
            	}
        	})
	}
	
})