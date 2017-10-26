$(document).ready(function() {
	
	$(".page-trigger").click(function() {
		$(".menu-trigger").removeClass("active");
		addLoading("#page");
		$.ajax({
			type: "GET",
			url: $(this).attr("page"),
			dataType: "json",
			success: function(data) {
				$("#page").html(parseHTML(data));
				delLoading("#page");
			},
			error: function(xhr, status, thrown) {
				console.log(thrown);
	        	window.alert(JSON.parse(xhr.responseText).error);
	        	delLoading("#page");
			}
		});
	});
	
	$(".menu-trigger").click(function() {
		$(".menu-trigger").removeClass("active");
		$(this).addClass("active");
		addLoading("#page");
		$.ajax({
			type: "GET",
			url: $(this).attr("page"),
			dataType: "json",
			success: function(data) {
				$("#page").html(parseHTML(data));
				delLoading("#page");
			},
			error: function(xhr, status, thrown) {
				console.log(thrown);
	        	window.alert(JSON.parse(xhr.responseText).error);
	        	delLoading("#page");
			}
		});
	});
	
	addLoading("#page");
	$.ajax({
		type: "GET",
		url: $("#brand-main").attr("page"),
		dataType: "json",
		success: function(data) {
			$("#page").html(parseHTML(data));
			delLoading("#page");
		},
		error: function(xhr, status, thrown) {
			console.log(thrown);
        	window.alert(JSON.parse(xhr.responseText).error);
        	delLoading("#page");
		}
	});
	
});
