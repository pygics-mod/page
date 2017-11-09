var page_preproc = null;
var page_postproc = null;
var page_errproc = null;

function page_parse(dom, id, page_url) {
	if (typeof dom == "object") {
		if ("tag" in dom) {
			var html = "";
			var attrs = dom.attrs;
			var elems = dom.elems;
			html += "<" + dom.tag;
			if (id != null) { attrs["id"] = id; }
			if (page_url != null) { attrs["page_url"] = page_url; }
			for (var key in attrs) {
				html += ' ' + key + '="' + attrs[key] + '"';
			}
			html += ">";
			for (var i = 0, elem; elem = elems[i]; i++) {
				var parsed = page_parse(elem);
				if (parsed !== null) { html += parsed; }
			}
			html += "</" + dom.tag + ">";
			return html;
		} else if ("reload" in dom) {
			for (var i = 0, id; id = dom.reload[i]; i++) { page_patch(id); }
			return null;
		} else if ("error" in dom) {
			console.log(dom.error);
			window.alert(dom.error);
			return null;
		} else {
			return null;
		}
	}
	return dom;
}

function page_patch(id) {
	var obj = $("#" + id);
	var url = obj.attr("page_url");
	$.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        beforeSend: function() {
        	if (page_preproc != null) { page_preproc(id); }
        },
        success: function(data) {
        	var parsed_html = page_parse(data, id, url);
        	if (parsed_html !== null) { obj.replaceWith(parsed_html); }
        	if (page_postproc != null) { page_postproc(id); }
        },
        error: function(xhr, status, thrown) {
        	console.log(status, xhr, thrown);
        	window.alert(status + " : " + thrown);
        	if (page_errproc != null) { page_errproc(id); }
        }
    });
}

function page_get(obj) {
	var url = obj.attr("page_url");
	var id = obj.attr("page_view");
	var view = $("#" + id);
	$.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        beforeSend: function() {
        	if (page_preproc != null) { page_preproc(id); }
        },
        success: function(data) {
        	var parsed_html = page_parse(data, id, url);
        	if (parsed_html !== null) { view.replaceWith(parsed_html); }
        	if (page_postproc != null) { page_postproc(id); }
        },
        error: function(xhr, status, thrown) {
        	console.log(status, xhr, thrown);
        	window.alert(status + " : " + thrown);
        	if (page_errproc != null) { page_errproc(id); }
        }
    });
}

function page_post(obj) {
	var url = obj.attr("page_url");
	var id = obj.attr("page_view");
	var view = $("#" + id);
	var fields = $("." + obj.attr("page_data"));
	var data = {};
	for (var i=0, field; field = fields[i]; i++) {
		switch (field.tagName.toLowerCase()) {
		case "input":
			data[field.name] = field.value;
			break;
		}
	}
	$.ajax({
		type: "POST",
		url: url,
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		data: JSON.stringify(data),
		beforeSend: function() {
        	if (page_preproc != null) { page_preproc(id); }
        },
        success: function(data) {
        	var parsed_html = page_parse(data, id, url);
        	if (parsed_html !== null) { view.replaceWith(parsed_html); }
        	if (page_postproc != null) { page_postproc(id); }
        },
        error: function(xhr, status, thrown) {
        	console.log(status, xhr, thrown);
        	window.alert(status + " : " + thrown);
        	if (page_errproc != null) { page_errproc(id); }
        }
	});
}

function page_put(obj) {
	var url = obj.attr("page_url");
	var id = obj.attr("page_view");
	var view = $("#" + id);
	var fields = $("." + obj.attr("page_data"));
	var data = {};
	for (var i=0, field; field = fields[i]; i++) {
		switch (field.tagName.toLowerCase()) {
		case "input":
			data[field.name] = field.value;
			break;
		}
	}
	$.ajax({
		type: "PUT",
		url: url,
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		data: JSON.stringify(data),
		beforeSend: function() {
        	if (page_preproc != null) { page_preproc(id); }
        },
        success: function(data) {
        	var parsed_html = page_parse(data, id, url);
        	if (parsed_html !== null) { view.replaceWith(parsed_html); }
        	if (page_postproc != null) { page_postproc(id); }
        },
        error: function(xhr, status, thrown) {
        	console.log(status, xhr, thrown);
        	window.alert(status + " : " + thrown);
        	if (page_errproc != null) { page_errproc(id); }
        }
	});
}

function page_delete(obj) {
	var url = obj.attr("page_url");
	var id = obj.attr("page_view");
	var view = $("#" + id);
	$.ajax({
        type: "DELETE",
        url: url,
        dataType: "json",
        beforeSend: function() {
        	if (page_preproc != null) { page_preproc(id); }
        },
        success: function(data) {
        	var parsed_html = page_parse(data, id, url);
        	if (parsed_html !== null) { view.replaceWith(parsed_html); }
        	if (page_postproc != null) { page_postproc(id); }
        },
        error: function(xhr, status, thrown) {
        	console.log(status, xhr, thrown);
        	window.alert(status + " : " + thrown);
        	if (page_errproc != null) { page_errproc(id); }
        }
    });
}
