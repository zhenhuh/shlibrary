$(function(){
    /**
     * 默认检索所有的物产
     */
    getDataList(null);

    //根据查询条件检索数据
    $("#single_search_btn_id").click(function(){
        getDataList({entity:"松子"});
    });

    /**
     * 根据查询条件检索数据
     */
    function getDataList(jsonData){
        $.ajax({
            url:"/index/leftfrm",
            type:"post",
            data:jsonData,
            dataType:"json",
            success:function(data){
                console.log("result:",data);
                if(data==null){
                    $("#m-list-search_results_id").html("<span class='m-list-search__result-message'>对不起，没有检索到相关数据 </span>");
                }else{
                    // var content ='<div style="margin-bottom:10px;">'+
                    //                 '<a href="/detail" target="_blank" class="m-list-search__result-item">'+
                    //                     '<span class="m-list-search__result-item-icon">'+
                    //                         '<i class="flaticon-paper-plane m--font-info"></i>'+
                    //                     '</span>'+
                    //                     '<span class="m-list-search__result-category m-list-search__result-category--first">'+
                    //                         '松子<i style="font-size:10px;margin-left:15px;">(明 景泰6年(1455))</i>'+
                    //                     '</span>'+
                    //                     '<span class="m-list-search__result-item-text">'+
                    //                         '来源志书1，来源志书2'+
                    //                     '</span>'+
                    //                 '</a>'+
                    //                 '<a href="#" class="m-list-search__result-item">'+
                                        
                    //                 '</a></div>';
                    var content ='<ul class="m-nav m-nav--inline">'+
                                    '<li class="m-nav__item">'+
                                        '<a href="/product_detail" target="_blank" class="m-nav__link">'+
                                            '<i class="flaticon-paper-plane m--font-info" style="padding-right:10px;"></i>'+
                                            '<span class="m-nav__link-text" style="font-size:16px;">'+
                                                '松子'+    
                                            '</span>'+
                                        '</a>'+
                                    '</li>'+
                                    '<li class="m-nav__item">'+
                                        '<span class="m-nav__link-text" style="padding-left:10px;">'+
                                            '来源志书1<i style="margin-left:15px;">(明 景泰6年(1455))</i>'+
                                        '</span>'+
                                    '</li>'+
                                '</ul>';

                    $("#m-list-search_results_id").empty();
                    $("#m-list-search_results_id").append(content);
                    $("#m-list-search_results_id").append(content);
                    $("#m-list-search_results_id").append(content);
                    $("#m-list-search_results_id").append(content);
                    $("#m-list-search_results_id").append(content);
                    $("#m-list-search_results_id").append(content);
                    $("#m-list-search_results_id").append(content);
                    $("#m-list-search_results_id").append(content);
                    $("#m-list-search_results_id").append(content);
                    $("#m-list-search_results_id").append(content);
                    
                    var btn = '<a style="float:right;" class="btn btn-info m-btn m-btn--custom m-btn--icon m-btn--pill m-btn--air">'+
                        '<span>'+
                            '<i class="la la-plus"></i>'+
                            '<span>'+
                                '点我查看更多'+
                            '</span>'+
                        '</span>'+
                    '</a>';
                    $("#m-list-search_results_id").append(btn);
                }
            },
            error:function(data){
                console.log("result:",data);
                alert("error");
            }
        });
    }
});

