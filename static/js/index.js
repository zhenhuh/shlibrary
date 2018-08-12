var advancedPageData = {};  //高级检索

$(function(){
    /**
     * 隐藏分页插件
     */
    $(".dataTables_wrapper").hide();

    /**
     * 默认检索所有的物产
     */
    getDataList();

    //加载右侧部分内容
    index_right.getList();

    /**
     * 简单搜索
     * name : 物产名称或来源支书
     * current_page : 结果当前所在页面
     */
    $("#single_search_btn_id").click(function(){
        var val = $("#wc_or_zs_name_id").val();
        if(val==null || val.trim() == ""){
            alert("请输入检索词!");
            return;
        }
        //清空查询结果列表
        $("#m-list-search_results_id").empty();
        advancedPageData = {
            name: $("#wc_or_zs_name_id").val(),
            current_page: 1,
            url:'/search_simple/'
        };
        searchByParam(advancedPageData);
    });

    /**
     * 高级搜索
     * name : 物产名称
     * year_start : 开始时间
     * year_end : 结束时间
     * source_lc : 来源志书
     * yn_region : 云南行政区域
     * current_page : 结果当前所在页面
     */
    $("#advanced_seache_btn_id").click(function(){
        advancedPageData = {
            name: $("#name_id").val(),
            year_start: $("#year_start_id").val(),
            year_end: $("#year_end_id").val(),
            source_lc: $("#source_lc_id").val(),
            yn_region: $("#yn_region_id").val(),
            current_page: 1,
            url:'/search/'
        };
        if((advancedPageData.name==null || advancedPageData.name=="") &&
            (advancedPageData.year_start==null || advancedPageData.year_start=="") &&
            (advancedPageData.year_end==null || advancedPageData.year_end=="") &&
            (advancedPageData.source_lc==null || advancedPageData.source_lc=="") &&
            (advancedPageData.yn_region==null || advancedPageData.yn_region=="")){
            alert("请至少输入一个检索词!");
            return;
        }
        $("#m-list-search_results_id").empty();
        searchByParam(advancedPageData);
    });

    /**
     * 默认检索数据
     */
    function getDataList(){
        $.ajax({
            url:"/index/leftfrm",
            type:"post",
            dataType:"json",
            success:function(data){
                
                $("#m-list-search_results_id").empty();
                if(data==null){
                    $("#m-list-search_results_id").html("<span class='m-list-search__result-message'>对不起，没有检索到相关数据 </span>");
                }else{
                    $(data.data).each(function(index,ele){
                        var content ='<ul class="m-nav m-nav--inline">'+
                                '<li class="m-nav__item">'+
                                    '<a href="/product_detail/?id='+ele.uid+'&name='+ele.product_name+'" target="_blank" class="m-nav__link">'+
                                        '<i class="flaticon-paper-plane m--font-info" style="padding-right:10px;"></i>'+
                                        '<span class="m-nav__link-text" style="font-size:16px;">'+
                                            ele.product_name +
                                        '</span>'+
                                    '</a>'+
                                '</li>'+
                                '<li class="m-nav__item">'+
                                    '<span class="m-nav__link-text" style="padding-left:10px;">'+
                                        ele.wcsource + '<i style="margin-left:15px;">'+ele.temporal+'</i>'+
                                    '</span>'+
                                '</li>'+
                            '</ul>';
                        $("#m-list-search_results_id").append(content);
                    });
                }
            },
            error:function(data){
                alert("error");
            }
        });
    }
});

    /**
     * 根据查询条件检索数据
     */
    function searchByParam(jsonData){
        /**
         * 显示分页插件
         */
        $(".dataTables_wrapper").show();
        var tempdata = {};
        $.extend(tempdata, jsonData);
        delete tempdata.url; 

        $.ajax({
            url:jsonData.url,
            type:"post",
            data: tempdata,
            dataType:"json",
            success:function(data){
                $.callbackPageinfo(data);
                if(data==null || data.count==0){
                    $("#m-list-search_results_id").append("<span class='m-list-search__result-message'>对不起，没有检索到相关数据 </span>");
                }else{                    
                    //加载页面数据
                    $(data.data).each(function(index,ele){
                        var content ='<ul class="m-nav m-nav--inline">'+
                                '<li class="m-nav__item">'+
                                    '<a href="/product_detail/?id='+ele.uid+'&name='+ele.product_name+'" target="_blank" class="m-nav__link">'+
                                        '<i class="flaticon-paper-plane m--font-info" style="padding-right:10px;"></i>'+
                                        '<span class="m-nav__link-text" style="font-size:16px;">'+
                                            ele.product_name +
                                        '</span>'+
                                    '</a>'+
                                '</li>'+
                                '<li class="m-nav__item">'+
                                    '<span class="m-nav__link-text" style="padding-left:10px;">'+
                                        ele.wcsource + '<i style="margin-left:15px;">'+ele.temporal+'</i>'+
                                    '</span>'+
                                '</li>'+
                            '</ul>';
                        $("#m-list-search_results_id").append(content);
                    });
                }
            },
            error:function(data){
                alert("error");
            }
        });
    }

    /**
     *查看更多
     */
    function searchByPageIndex(advancedPageData){
        $("#m-list-search_results_id").empty();
        searchByParam(advancedPageData);
    }