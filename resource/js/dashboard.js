$(document).ready(function() {
	var dashboard_page_fix = $("#dashboard-page-fix");
	dashboard_page_fix.css("width", dashboard_page_fix.parent().width() + 15 + 'px');
});

$(window).resize(function() {
	var dashboard_page_fix = $("#dashboard-page-fix");
	dashboard_page_fix.css("width", dashboard_page_fix.parent().width() + 15 + 'px');
});