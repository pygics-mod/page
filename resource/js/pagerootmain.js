
function clickThumbnailStar(star) {
	var title = star.attr("title");
	var target = star.attr("target");
	var show_inner = $("#root-page-show-inner");
	if (star.hasClass("fa-star-o")) {
		star.removeClass("fa-star-o").addClass("fa-star");
		$(".item").removeClass("active prev next left right");
		show_inner.append('<div class="item active" title="' + title + '" target="' + target + '"><iframe class="root-page-inner" src="' + target + '"></iframe></div>');
		$(".root-page-inner-blank").remove();
	} else {
		star.removeClass("fa-star").addClass("fa-star-o");
		show_inner.children().each(function() {
			if($(this).attr("target") == target && $(this).attr("title") == title) {
				$(this).remove();
			}
		});
		if (show_inner.children().length == 0) {
			show_inner.append('<div class="item root-page-inner-blank" target="#"><img src="/page/resource/image/pygics_logo_96.png"><div>Page.</div></div>');
		}
		show_inner.children().first().addClass("active");
	}
};

function clickThumbnailRemove(thumbnail) {
	var title = thumbnail.attr("title");
	var target = thumbnail.attr("target");
	var show_inner = $("#root-page-show-inner");
	show_inner.children().each(function() {
		if($(this).attr("target") == target && $(this).attr("title") == title) {
			$(this).remove();
		}
	});
	if (show_inner.children().length == 0) {
		show_inner.append('<div class="item root-page-inner-blank" target="#"><img src="/page/resource/image/pygics_logo_96.png"><div>Page.</div></div>');
	}
	show_inner.children().first().addClass("active");
	thumbnail.parent().parent().remove();
	var pageroot_cookie = Cookies.getJSON("pageroot");
	var index = null;
	pageroot_cookie.thumbnails.forEach(function (v, i) {
		if (v.name == title && v.target == target) {
			index = i;
		}
	});
	if (index != null) {
		pageroot_cookie.thumbnails.splice(index, 1);
	}
	Cookies.set("pageroot", pageroot_cookie);
};

function clickThumbnail(thumbnail) {
	window.open(thumbnail.children("iframe").first().attr("src"), '_blank').focus();
};

function createThumbnail(name, target, star) {
	var isExist = false;
	$("#thumbnail-list").children().each(function() {
		if($(this).attr("target") == target) {
			alert("Already Exist URL!");
			isExist = true;
		}
	});
	if(!isExist) {
		var str = '';
		str += '<div class="thumbnail-container" title="' + name + '" target="' + target + '">';
		str += '<div class="thumbnail-control">';
		str += '<i class="fa fa-2x fa-remove thumbnail-control-remove" title="' + name + '" target="' + target + '" onclick="clickThumbnailRemove($(this));"></i>';
		str += '<div class="thumbnail-control-title">' + name + '</div>';
		str += '<div class="thumbnail-control-star-container">';
		str += '<i class="fa fa-2x fa-star-o thumbnail-control-star" title="' + name + '" target="' + target +'" onclick="clickThumbnailStar($(this));"></i>';
		str += '</div></div>';
		str += '<div class="thumbnail" onclick="clickThumbnail($(this));">';
		str += '<iframe src="' + target + '"></iframe>';
		str += '</div></div>';
		$("#thumbnail-list").append(str);
		var pageroot_cookie = Cookies.getJSON("pageroot");
		pageroot_cookie.thumbnails.push({name: name, target: target});
		Cookies.set("pageroot", pageroot_cookie);
	};
};

$(document).ready(function() {
	
	$(".thumbnail-control-star").click(function() {
		clickThumbnailStar($(this));
	});
	
	$(".thumbnail").click(function() {
		clickThumbnail($(this));
	});
	
	$("#add-page-submit").click(function() {
		var name = $("#add-page-name").val();
		var url = $("#add-page-url").val();
		if (name != "" && url != "") {
			$("#add-page-name").val("");
			$("#add-page-url").val("");
			createThumbnail(name, url);
		}
	});
	
	var pageroot_cookie = Cookies.getJSON("pageroot");
	Cookies.set("pageroot", {thumbnails: []}, {expires: 2147483647});
	if (pageroot_cookie != null) {
		pageroot_cookie.thumbnails.forEach(function(v, i) {
			createThumbnail(v.name, v.target);
		});
	};
});
