/**
 * 首页右侧部分数据检索
 * 动态展示右侧数据
 */
var index_right = {
    /**
     * 首页右侧部分内容检索
     */
    getList:function(){
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
                        letterContent += '<a href="javascript:;" id="letter_link_'+index+'" style="margin-left:20px;"><i>'+
                                ele.letter+'('+ ele.count+')</i></a>';
                    });
                    $("#firstLetter_id").append(letterContent);
                    $("#firstLetter_id").append("</p>");
                    //隐藏三行之后的数据
                    $("#firstLetter_id").find("p:gt(3)").hide(t);
                    //查询数据
                    $("#firstLetter_id").find("a[id^=letter_link_]").click(function(){
                        index_right.index_right_click({
                            url:"/index/rightfrm_letter_click/",
                            data:{
                                current_letter:$(this).find("i").text().trim().substring(0,1),
                                current_page: 1
                            }
                        });
                    });

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
                        taxonomyContent += '<a href="javascript:;" id="taxonomy_link_'+index+'" style="margin-left:20px;"><i>'+ele.taxonomy+'</i></a>';
                    });
                    $("#taxonomy_id").append(taxonomyContent);
                    $("#taxonomy_id").append("</p>");
                    //查询数据
                    $("#taxonomy_id").find("a[id^=taxonomy_link_]").click(function(){
                        index_right.index_right_click({
                            url:"/index/rightfrm_taxonomy_click/",
                            data:{
                                current_taxonomy:$(this).find("i").text().trim(),
                                current_page: 1
                            }
                        });
                    });

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
                        regionContent += '<a href="javascript:;" id="region_link_'+index+'" style="margin-left:20px;"><i>'+ele.region+'</i></a>';
                    });
                    $("#region_id").append(regionContent);
                    $("#region_id").append("</p>");
                     //查询数据
                    $("#region_id").find("a[id^=region_link_]").click(function(){
                        index_right.index_right_click({
                            url:"/index/rightfrm_region_click/",
                            data:{
                                current_region:$(this).find("i").text().trim(),
                                current_page: 1
                            }
                        });
                    });
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
    },

    /**
     * 右侧部分点击事件
     */
    index_right_click:function(jsonData){
        $.ajax({
            url:jsonData.url,
            type:"post",
            data: jsonData.data,
            dataType:"json",
            success:function(data){
                //清空左侧部分列表数据
                $("#m-list-search_results_id").empty();
                if(data==null){
                    $("#m-list-search_results_id").html("<span class='m-list-search__result-message'>对不起，没有检索到相关数据 </span>");
                }else{
                    var wccontent = '<div class="m-portlet">'+
                                    '<div class="m-portlet__body  m-portlet__body--no-padding">'+
                                    '<div class="row m-row--no-padding m-row--col-separator-xl">';
                    $(data.data).each(function(index,ele){
                        if(index >0 && index % 4 == 0){
                            wccontent +='</div><div class="row m-row--no-padding m-row--col-separator-xl">';
                        }
                        wccontent +='<div class="col-md-12 col-lg-6 col-xl-3">'+
                                    '<div class="m-widget24">'+
                                        '<div class="m-widget24__item" style="text-align:center;"> '+
                                            '<a href="javascript:;" wcname="'+ele.wcname+'" class="wc_list_link">'+
                                            '<h4 class="jiugongge_css"><i class="flaticon-layers m--font-warning"></i>    '+
                                                ele.wcname +
                                            '</h4></a>'+
                                            '<br>'+
                                        '</div>'+
                                    '</div>'+
                                '</div>';
                    });
                    $("#m-list-search_results_id").append(wccontent);
                    $("#m-list-search_results_id").append("</div></div></div>");
                    //连接到简单检索
                    $(".wc_list_link").click(function(){
                        var wcname = $(this).attr("wcname");
                        $("#wc_or_zs_name_id").val(wcname);
                        $("#single_search_btn_id").click();
                    });
                }
            },
            error:function(data){
                alert("error");
            }
        });
    }
}
