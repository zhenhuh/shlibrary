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
                    var content ='<a href="/detail" target="_blank">'+
                                    '<span class="m-list-search__result-category m-list-search__result-category--first">'+
                                        '松子<i style="font-size:10px;margin-left:15px;">(明 景泰6年(1455))</i>'+
                                    '</span>'+
                                '</a>'+
                                '<a href="#" class="m-list-search__result-item">'+
                                    '<span class="m-list-search__result-item-icon">'+
                                        '<i class="flaticon-interface-3 m--font-warning"></i>'+
                                    '</span>'+
                                    '<span class="m-list-search__result-item-text">'+
                                        '树皮無龍鳞而稍光滑枝上結松毬大如茶甌其中含寶有二三百粒者'+
                                    '</span>'+
                                '</a>';

                    $("#m-list-search_results_id").empty();
                    $("#m-list-search_results_id").append(content);
                }
            },
            error:function(data){
                console.log("result:",data);
                alert("error");
            }
        });
    }
});

