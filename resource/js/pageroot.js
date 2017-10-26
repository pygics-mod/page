$(document).ready(function() {
	// Button Events
	$("#root-page-menu-down").click(function() {
		if(!$("#root-page-menu").hasClass("active")) {
			if($("#root-page-menu-ar-ctrl").hasClass("fa-pause")) {
				$("#root-page-show").carousel("pause");
			}
			$("#root-page-menu").addClass("active")
			if(window.innerHeight >= 400) {
				$("#root-page-menu").animate({top:"+="+window.innerHeight}, 400);
			} else {
				$("#root-page-menu").animate({top:"+=400"}, 400);
			}
		}
	});
	
	$("#root-page-menu-up").click(function() {
		if($("#root-page-menu").hasClass("active")) {
			if($("#root-page-menu-ar-ctrl").hasClass("fa-pause")) {
				$("#root-page-show").carousel("cycle");
			}
			$("#root-page-menu").removeClass("active")
			if(window.innerHeight >= 400) {
				$("#root-page-menu").animate({top:"-="+window.innerHeight}, 400);
			} else {
				$("#root-page-menu").animate({top:"-=400"}, 400);
			}
		}
	});
	
	$("#root-page-menu-ar-ctrl").click(function() {
		if($(this).hasClass("fa-pause")) {
			$(this).removeClass("fa-pause").addClass("fa-play");
		} else {
			$(this).removeClass("fa-play").addClass("fa-pause");
		}
	});
	
	$("#root-page-menu-ar-up").click(function() {
		var sec = parseInt($("#root-page-menu-ar-sec").attr("ar-sec"));
		if (sec < 60) {
			sec += 1;
			$("#root-page-menu-ar-sec").attr("ar-sec", sec).html(sec);
			var c = $("#root-page-show");
			var opt = c.data()["bs.carousel"].options;
			opt.interval = sec * 1000;
			c.data({options: opt});
		}
	});
	
	$("#root-page-menu-ar-down").click(function() {
		var sec = parseInt($("#root-page-menu-ar-sec").attr("ar-sec"));
		if (sec > 1) {
			sec -= 1;
			$("#root-page-menu-ar-sec").attr("ar-sec", sec).html(sec);
			var c = $("#root-page-show");
			var opt = c.data()["bs.carousel"].options;
			opt.interval = sec * 1000;
			c.data({options: opt});
		}
	});
	
	$("#root-page-show-control-left").hover(
		function() {$(this).animate({left:"+=80"}, 200);},
		function() {$(this).animate({left:"-=80"}, 200);}
	);
	
	$("#root-page-show-control-right").hover(
		function() {$(this).animate({right:"+=80"}, 200);},
		function() {$(this).animate({right:"-=80"}, 200);}
	);
	
	// Initial Running
	$("#root-page-show").carousel({interval:5000});
	
	if(!$("#root-page-menu").hasClass("active")) {
		if (window.innerHeight >= 400) {
			$("#root-page-menu").css("height", "calc(100% + 15px)").css("top", "-100%");
		} else {
			$("#root-page-menu").css("height", "415px").css("top", '-400px');
		}
	}
	
	$.ajax({
		type: "GET",
		url: "/page/root_page_main",
		dataType: "json",
		success: function(data) {
			$("#page").html(parseHTML(data));
		},
		error: function(xhr, status, thrown) {
			console.log(thrown);
        	window.alert(JSON.parse(xhr.responseText).error);
		}
	});
});

// Window Resizing
$(window).resize(function() {
	$("#root-page-show-control-right").css("left", "auto");
	if (window.innerHeight >= 400) {
		$("#root-page-menu").css("height", "calc(100% + 15px)");
		if(!$("#root-page-menu").hasClass("active")) {
			$("#root-page-menu").css("top", "-100%");
		}
	} else {
		$("#root-page-menu").css("height", "415px");
		if(!$("#root-page-menu").hasClass("active")) {
			$("#root-page-menu").css("top", '-400px');
		}
	}
});