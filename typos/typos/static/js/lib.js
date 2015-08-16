function submit_new() {
	var webName = $("#webName").val();
	var link = $("#link").val();
	var inWord = $("#inWord").val();
	var inCentence = $("#inCentence").val();
	var correctWord = $("#correctWord").val();
	var corpName = $("#corpName option:selected").val();
	
	$.ajax({
        type: "POST",   //访问WebService使用Post方式请求
        url: '/submit/', //调用WebService的地址和方法名称组合 ---- WsURL/方法名
        data: {webName: webName,
        	link: link,
        	inWord: inWord,
        	inCentence: inCentence,
        	correctWord: correctWord,
        	corpName: corpName
        },
        dataType: 'json',   //WebService 会返回Json类型
        success: function(result) {     //回调函数，result，返回值
    		alert('提交成功!');
            window.location.href = '\\';
        }
	});
}