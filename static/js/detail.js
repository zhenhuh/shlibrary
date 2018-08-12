/**
 * 详细页面JS文件
 */
$(function() {

    /**
     * 查询明细数据
     */
    $.ajax({
        url:"/product_detail_test/",
        type:"post",
        dataType:"json",
        data:{
                id:$("#product_id").val(),
                name:$("#product_name").val()
            },
        success:function(data){
            //设置详细信息
            setDetailData(data);
            //展示地图
            showDetailPlace(data.map_location);
        },
        error:function(data){

        }
    });

    /**
     * 详细页面赋值
     * @param  data 
     */
    function setDetailData(data){
        $("#product_name_id").text(data.product_name);//物产名
        //物产来源方志
        var wcsource_fz = "";
        if(data.wcsource_fz != null && data.wcsource_fz!=""){
            wcsource_fz = "<a href='/fz_detail/?name="+data.wcsource_fz+"&wtime="+data.wtime+"' target='_blank'>"+data.wcsource_fz+"</a>";
        }else{
            wcsource_fz = "无";
        }
        $("#wcsource_fz_id").append(wcsource_fz); 
        //物产来源其他古籍
        var wcsource_qt = "";
        if(data.beautify_wcsource_qt != null && data.beautify_wcsource_qt!=""){
            wcsource_qt = data.beautify_wcsource_qt;
        }else{
            wcsource_qt = "无";
        }
        $("#wcsource_qt_id").text(wcsource_qt);

        //物产所属分类标签
        var category_qt = "";
        if(data.category_qt != null && data.category_qt!=""){
            category_qt = data.category_qt;
        }else{
            category_qt = "无";
        }
        $("#category_qt_id").text(category_qt);

        //物产相关人物-格式问题 -todo
        if(data.Des_people != null && data.Des_people != ""){
            $("#Des_people_id").append("<a href='/shlib/person/?person='"+data.Des_people+">");
        }else{
            $("#Des_people_id").append("无");
        }
        
        //物产描述
        if(data.desc != null && data.desc != ""){
            //描述信息
            $("#desc_id").append("<h6>方志物产描述:</h6>");
            $("#desc_id").append(data.desc);
            $("#desc_id").append("<br/>");
        }

        //其他古籍描述
        if(!jQuery.isEmptyObject(data.gjdesc)){
            //描述信息
            $("#desc_id").append("<br/><h6>其他古籍物产描述:</h6>");
            for(var key in data.gjdesc){
                $("#desc_id").append("<span style='margin-left:15px;'>"+key+":</span><span>"+data.gjdesc[key]+"</span>");
                $("#desc_id").append("<br/>");
            }
        }
        
        //诗句
        if(data.poems != null && data.poems.count > 0){
            var poems = "";
            var poedata = data.poems.data;
            $("#desc_id").append("<br/><h6>相关诗句:</h6>");
            for(var i in poedata){
                //诗句
                $("#desc_id").append("<span style='margin-left:15px;'>"+poedata[i].author+"-《"+poedata[i].title+"》-"+poedata[i].clause+"</span>");
                $("#desc_id").append("<br/>");
            }
        }
        /**
         * 百科字段
         */
        if(!jQuery.isEmptyObject(data.wiki_info)){
            var wiki_info = "";
            //百度百科
            if(data.wiki_info.baidubaike != null){
                $("#wiki_info_id").append("<h6>百度百科:</h6>");
                var baidu = data.wiki_info.baidubaike;
                //abstracts relatedImage
                if(baidu.abstracts != null){
                    $("#wiki_info_id").append("<span>"+baidu.abstracts+"</span>");
                }
                if(baidu.relatedImage != null){
                    for(var i in baidu.relatedImage){
                        $("#wiki_info_id").append("<img src='"+baidu.relatedImage[i]+"' />");
                    }
                }
            }
            //互动百科
            if(data.wiki_info.hudongbaike != null){
                $("#wiki_info_id").append("<h6>互动百科:</h6>");
                var hudong = data.wiki_info.hudongbaike;
                
                if(hudong.abstracts != null){
                    $("#wiki_info_id").append("<span>"+hudong.abstracts+"</span>");
                }
                if(hudong.relatedImage != null){
                    for(var i in hudong.relatedImage){
                        $("#wiki_info_id").append("<img src='"+hudong.relatedImage[i]+"' />");
                    }
                }
            }
            //中国维基
            if(data.wiki_info.zhwiki != null){
                $("#wiki_info_id").append("<h6>中国维基:</h6>");
                var wiki = data.wiki_info.zhwiki;
                
                if(wiki.abstracts != null){
                    $("#wiki_info_id").append("<span>"+wiki.abstracts+"</span>");
                }
                if(wiki.relatedImage != null){
                    for(var i in wiki.relatedImage){
                        $("#wiki_info_id").append("<img src='"+wiki.relatedImage[i]+"' />");
                    }
                }
            }
        }else{
            $("#wiki_info_id").text("无");
        }
    }

    function showDetailPlace(data){
        var map = new BMap.Map("yn_map");
        var point = new BMap.Point(data.longitude,data.latitude);
        map.centerAndZoom(point, 8);
        map.enableScrollWheelZoom();
        var marker = new BMap.Marker(point);  // 创建标注
        
        map.addOverlay(marker);               // 将标注添加到地图中
        marker.setAnimation(BMAP_ANIMATION_BOUNCE); //跳动的动画
    
        var opts = {
            position :point,    // 指定文本标注所在的地理位置
            offset   : new BMap.Size(20, -10)    //设置文本偏移量
        }
        var label = new BMap.Label(data.place,opts);
        marker.setLabel(label);
    }
});