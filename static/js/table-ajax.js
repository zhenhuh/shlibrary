var DatatableRemoteAjax = {
    init: function() {
        var t;
        t = $(".m_datatable").mDatatable({
            data: {
                type: "remote",
                source: {
                    read: {
                        url: "/fzstat/",
                        map: function(t) {
                            var e = t;
                            return void 0 !== t.data && (e = t.data),
                            e
                        }
                    }
                },
                pageSize: 10,
                serverPaging: !0,
                serverFiltering: !0,
                serverSorting: !0
            },
            layout: {
                scroll: !1,
                footer: !1
            },
            sortable: !0,
            pagination: !0,
            
            // search: {
            //     input: $("#generalSearch")
            // },
            
            columns: [{
                field: "area",
                filterable: !0,
                sortable: !1,
                title: "地理位置"
            },
            {
                field: "bookname",
                filterable: !0,
                sortable: !1,
                title: "志书名称"
                
            },
            {
                field: "count_wc",
                filterable: !0,
                sortable: !1,
                title: "物产总量"
            },
            {
                field: "type",
                filterable: !0,
                sortable: !1,
                title: "志书类型"
            }]
        })
                
        // $("#generalSearch").on("change",
        // function() {
        //     t.search($(this).val(), "bookname")
        // })   
    }
};
jQuery(document).ready(function() {
    DatatableRemoteAjax.init()
});