var advancedPageData = {};  //高级检索

$(function(){
    /**
     * 默认检索所有的物产
     */
    getDataList();

    //加载右侧部分内容
    getRightDataList();

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
            current_page: 1
        };
        searchByParam(advancedPageData,'/search_simple/');
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
            current_page: 1
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
        searchByParam(advancedPageData,'/search/');
    });

    /**
     * 首页右侧部分内容检索
     */
    function getRightDataList(){
        var t = 400;
        $.ajax({
            url:"/index/rightfrm",
            type:"post",
            dataType:"json",
            success:function(data){
                if(data == null){

                }else{
                    //首字母
                    var letterContent = "<p>";
                    $(data.letter).each(function(index,ele){
                        if(index % 4 == 0){
                            letterContent +='</p><p>';
                        }
                        letterContent += '<i style="margin-left:20px;">'+ele.letter+'('+ ele.count+')</i>';
                    });
                    $("#firstLetter_id").append(letterContent);
                    $("#firstLetter_id").append("</p>");
                    //隐藏三行之后的数据
                    $("#firstLetter_id").find("p:gt(3)").hide(t);
                    //动态显隐
                    $("#firstLetter_more_id").click(function(){
                        if($("#firstLetter_id").find("p:eq(4)").is(":hidden")){
                            $("#firstLetter_id").find("p:gt(3)").show(t);
                        }else{
                            $("#firstLetter_id").find("p:gt(3)").hide(t);
                        }
                    });

                    //分类标签
                    var taxonomyContent = "<p>";
                    $(data.taxonomy).each(function(index,ele){
                        if(index % 4 == 0){
                            taxonomyContent +='</p><p>';
                        }
                        taxonomyContent += '<i style="margin-left:20px;">'+ele.taxonomy+'</i>';
                    });
                    $("#taxonomy_id").append(taxonomyContent);
                    $("#taxonomy_id").append("</p>");
                    //隐藏三行之后的数据
                    $("#taxonomy_id").find("p:gt(3)").hide(t);
                    //动态显隐
                    $("#taxonomy_more_id").click(function(){
                        if($("#taxonomy_id").find("p:eq(4)").is(":hidden")){
                            $("#taxonomy_id").find("p:gt(3)").show(t);
                        }else{
                            $("#taxonomy_id").find("p:gt(3)").hide(t);
                        }
                    });


                    //云南地区
                    var regionContent = "<p>";
                    $(data.region).each(function(index,ele){
                        if(index % 3 == 0){
                            regionContent +='</p><p>';
                        }
                        regionContent += '<i style="margin-left:20px;">'+ele.region+'</i>';
                    });
                    $("#region_id").append(regionContent);
                    $("#region_id").append("</p>");
                    //隐藏三行之后的数据
                    $("#region_id").find("p:gt(3)").hide(t);
                    //动态显隐
                    $("#region_more_id").click(function(){
                        if($("#region_id").find("p:eq(4)").is(":hidden")){
                            $("#region_id").find("p:gt(3)").show(t);
                        }else{
                            $("#region_id").find("p:gt(3)").hide(t);
                        }
                    });
                }
            },
            error:function(data){
                alert("error");
            }
        });
    }

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
                                    '<a href="/product_detail" target="_blank" class="m-nav__link">'+
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
    function searchByParam(jsonData,url){
        console.log("jsonData:",jsonData);
        $.ajax({
            url:url,
            type:"post",
            data:jsonData,
            dataType:"json",
            success:function(data){
                console.log(data);
                $.callbackPageinfo(data);
                if(data==null || data.count==0){
                    $("#m-list-search_results_id").append("<span class='m-list-search__result-message'>对不起，没有检索到相关数据 </span>");
                     //当前页码信息
                     $("#page_data_info_id").text("物产信息");
                }else{
                    //当前页码信息
                    $("#page_data_info_id").text("物产信息：共"+data.count+"条，当前页面从1条至"+(data.last_index+1)+"条");

                    //加载页面数据
                    $(data.data).each(function(index,ele){
                        var content ='<ul class="m-nav m-nav--inline">'+
                                '<li class="m-nav__item">'+
                                    '<a href="/product_detail" target="_blank" class="m-nav__link">'+
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
                    //判断是否还有下一页
                    var info = "";
                    if(data.page_next){
                        info = '<a style="float:right;" id="index_page_more_id" class="btn btn-info m-btn m-btn--custom m-btn--icon m-btn--pill m-btn--air" onclick="searchMore('+data.current_page+','+url+')" >'+
                            '<span>'+
                                '<i class="la la-plus"></i>'+
                                '<span>'+
                                    '点我加载更多' +
                                '</span>'+
                            '</span>'+
                        '</a>';
                    }else{
                        info = '<a style="float:right;" class="btn btn-info m-btn m-btn--custom m-btn--icon m-btn--pill m-btn--air">'+
                            '<span>'+
                                '<span>'+
                                    '没有更多了' +
                                '</span>'+
                            '</span>'+
                        '</a>';
                    }
                    
                    $("#m-list-search_results_id").append(info);
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
    function searchMore(current_page,url){
        $("#index_page_more_id").remove();
        
        advancedPageData.current_page = current_page + 1;
        searchByParam(advancedPageData,url);
    }