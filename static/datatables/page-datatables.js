function datatable_flush_draw(id) {
	var obj = $("#" + id);
	if (preproc != null) { preproc(id); }
	obj.DataTable({
		initComplete: function () { if (postproc != null) { postproc(id); } },
        lengthMenu: [
            [ 10, 25, 50, -1 ],
            [ '10 rows', '25 rows', '50 rows', 'Show all' ]
        ],
        destroy: true
	});
}

function datatable_sync_draw(id) {
	var obj = $("#" + id);
	if (preproc != null) { preproc(id); }
	obj.DataTable({
		ajax: obj.attr("page_url"),
		initComplete: function () { if (postproc != null) { postproc(id); } },
        lengthMenu: [
            [ 10, 25, 50, -1 ],
            [ '10 rows', '25 rows', '50 rows', 'Show all' ]
        ],
        destroy: true
	});
}

//$(view).DataTable({
//	ajax: $(view).attr("view"),
//	initComplete: function () { delLoading(view); },
//	scrollX: false,
//	dom: 'Bfrtip',
//    lengthMenu: [
//        [ 10, 25, 50, -1 ],
//        [ '10 rows', '25 rows', '50 rows', 'Show all' ]
//    ],
//    buttons: [
//    	{extend:'pageLength', text:'<i class="fa fa-align-justify"></i>', titleAttr:'Rows'},
//        {extend:'colvis', text:'<i class="fa fa-th-list"></i>', titleAttr:'Cols'},
//        {extend:'excelHtml5', text:'<i class="fa fa-file-excel-o"></i>', titleAttr:'Excel'},
//        {extend:'pdfHtml5', text:'<i class="fa fa-file-pdf-o"></i>', titleAttr:'PDF'},
//        {extend:'print', text:'<i class="fa fa-print"></i>', titleAttr:'Print'}
//    ],
//    order: [],
//    search: { "regex": false },
//    destroy: true
//});
//
//$(view).DataTable({
//	ajax: $(view).attr("view"),
//	initComplete: function () { delLoading(view); },
//	processing: true,
//	serverSide: true,
//	scrollX: false,
//	dom: 'Bfrtip',
//    lengthMenu: [
//        [ 10, 25, 50, -1 ],
//        [ '10 rows', '25 rows', '50 rows', 'Show all' ]
//    ],
//    buttons: [
//    	{extend:'pageLength', text:'<i class="fa fa-align-justify"></i>', titleAttr:'Rows'},
//        {extend:'colvis', text:'<i class="fa fa-th-list"></i>', titleAttr:'Cols'},
//        {extend:'excelHtml5', text:'<i class="fa fa-file-excel-o"></i>', titleAttr:'Excel'},
//        {extend:'pdfHtml5', text:'<i class="fa fa-file-pdf-o"></i>', titleAttr:'PDF'},
//        {extend:'print', text:'<i class="fa fa-print"></i>', titleAttr:'Print'}
//    ],
//    searchDelay: 1000,
//    search: { "regex": false },
//    destroy: true
//});