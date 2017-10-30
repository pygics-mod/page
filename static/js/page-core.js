var preproc = null;
var postproc = null;

function parse_dom(dom) {
	if (typeof dom == "object") {
		if ("error" in dom) {
			console.log(dom.error);
			window.alert(dom.error);
			return ""
		}
		var html = "";
		var attrs = dom.attrs;
		var elems = dom.elems;
		html += "<" + dom.tag;
		for (var key in attrs) {
			html += ' ' + key + '="' + attrs[key] + '"';
		}
		html += ">";
		for (var i = 0, elem; elem = elems[i]; i++) {
			html += parse_dom(elem);
		}
		html += "</" + dom.tag + ">";
		return html;
	}
	return dom;
}

function patch_dom(id) {
	var _id = "#" + id;
	$.ajax({
        type: "GET",
        url: $(_id).attr("page_url"),
        dataType: "json",
        beforeSend: function() {
        	if (preproc != null) { preproc(id); }
        },
        success: function(data) {
        	$(_id).html(parse_dom(data));
        	if (postproc != null) { postproc(id); }
        },
        error: function(xhr, status, thrown) {
        	$(_id).html("");
        	console.log(status, xhr, thrown);
        	window.alert(status + " : " + thrown);
        	if (postproc != null) { postproc(id); }
        }
    });
}

function replace_dom(id) {
	var _id = "#" + id;
	$.ajax({
        type: "GET",
        url: $(_id).attr("page_url"),
        dataType: "json",
        beforeSend: function() {
        	if (preproc != null) { preproc(id); }
        },
        success: function(data) {
        	$(_id).replaceWith(parse_dom(data));
        	if (postproc != null) { postproc(id); }
        },
        error: function(xhr, status, thrown) {
        	$(_id).html("");
        	console.log(status, xhr, thrown);
        	window.alert(status + " : " + thrown);
        	if (postproc != null) { postproc(id); }
        }
    });
}

//function patchView(view) {
//	addLoading(view);
//	$.ajax({
//        type: "GET",
//        url: $(view).attr("view"),
//        dataType: "json",
//        success: function(data) {
//        	$(view).replaceWith(parseHTML(data));
//            delLoading(view);
//        },
//        error: function(xhr, status, thrown) {
//        	console.log(thrown);
//        	window.alert(JSON.parse(xhr.responseText).error);
//        	delLoading(view);
//        }
//    });
//};
//
//function signalView(trig, view) {
//	$(trig).click(function() {
//		addLoading(view);
//        $.ajax({
//            type: $(trig).attr("method"),
//            url: $(trig).attr("view"),
//            dataType: "json",
//            success: function(data) {
//            	$(view).replaceWith(parseHTML(data));
//                delLoading(view);
//            },
//            error: function(xhr, status, thrown) {
//            	console.log(thrown);
//            	window.alert(JSON.parse(xhr.responseText).error);
//            	delLoading(view);
//            }
//        });
//    });
//};
//
//function contextView(trig, view) {
//	$(trig).click(function() {
//		var context = $(this).attr("context");
//		var data = {};
//		$(context).each(function(index) {
//			var d = $(this).val();
//			if (d == "" && $(this).attr("placeholder") !== typeof undefined) {
//				d = $(this).attr("placeholder");
//			}
//			data[$(this).attr("name")] = d;
//			if ($(this)[0].tagName == "INPUT") {
//				$(this).val("");
//			}
//		});
//		addLoading(view);
//		$.ajax({
//			type: "POST",
//			url: $(trig).attr("view"),
//			contentType: "application/json; charset=utf-8",
//			dataType: "json",
//			data: JSON.stringify(data),
//			success: function(data) {
//				$(view).replaceWith(parseHTML(data));
//            	delLoading(view);
//	        },
//	        error: function(xhr, status, thrown) {
//	        	console.log(thrown);
//	        	window.alert(JSON.parse(xhr.responseText).error);
//	        	delLoading(view);
//	        }
//		});
//	});
//};
//
//function tableView(view) {
//	if ($(view).attr("proc") == "sync") {
//		addLoading(view);
//		$(view).DataTable({
//			ajax: $(view).attr("view"),
//			initComplete: function () { delLoading(view); },
//			scrollX: false,
//	    	dom: 'Bfrtip',
//	        lengthMenu: [
//	            [ 10, 25, 50, -1 ],
//	            [ '10 rows', '25 rows', '50 rows', 'Show all' ]
//	        ],
//	        buttons: [
//	        	{extend:'pageLength', text:'<i class="fa fa-align-justify"></i>', titleAttr:'Rows'},
//	            {extend:'colvis', text:'<i class="fa fa-th-list"></i>', titleAttr:'Cols'},
//	            {extend:'excelHtml5', text:'<i class="fa fa-file-excel-o"></i>', titleAttr:'Excel'},
//	            {extend:'pdfHtml5', text:'<i class="fa fa-file-pdf-o"></i>', titleAttr:'PDF'},
//	            {extend:'print', text:'<i class="fa fa-print"></i>', titleAttr:'Print'}
//	        ],
//	        order: [],
//	        search: { "regex": false },
//	        destroy: true
//	    });
//	}
//	else if ($(view).attr("proc") == "async") {
//		addLoading(view);
//		$(view).DataTable({
//			ajax: $(view).attr("view"),
//			initComplete: function () { delLoading(view); },
//			processing: true,
//			serverSide: true,
//			scrollX: false,
//	    	dom: 'Bfrtip',
//	        lengthMenu: [
//	            [ 10, 25, 50, -1 ],
//	            [ '10 rows', '25 rows', '50 rows', 'Show all' ]
//	        ],
//	        buttons: [
//	        	{extend:'pageLength', text:'<i class="fa fa-align-justify"></i>', titleAttr:'Rows'},
//	            {extend:'colvis', text:'<i class="fa fa-th-list"></i>', titleAttr:'Cols'},
//	            {extend:'excelHtml5', text:'<i class="fa fa-file-excel-o"></i>', titleAttr:'Excel'},
//	            {extend:'pdfHtml5', text:'<i class="fa fa-file-pdf-o"></i>', titleAttr:'PDF'},
//	            {extend:'print', text:'<i class="fa fa-print"></i>', titleAttr:'Print'}
//	        ],
//	        searchDelay: 1000,
//	        search: { "regex": false },
//	        destroy: true
//	    });
//	}
//};