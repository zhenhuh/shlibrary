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
        console.log(data);
        $("#product_name_id").text(data.product_name);//物产名
        //物产来源方志
        var wcsource_fz = "";
        if(data.wcsource_fz != null && data.wcsource_fz.trim()!=""){
            wcsource_fz = "<a href='/fz_detail/?name="+data.wcsource_fz.trim()+"&wtime="+data.wtime+"' target='_blank'>"+data.wcsource_fz.trim()+"</a>"+
                "——<span>"+data.temporal+"</span>";
        }else{
            wcsource_fz = "无";
        }
        $("#wcsource_fz_id").append(wcsource_fz); 
        console.log(data);
        //物产来源其他古籍
        var wcsource_qt = data.wcsource_qt;
        if(wcsource_qt != null && wcsource_qt.length>0){
            var wcs_arr = wcsource_qt.split(";");
            for(var i in wcs_arr){
                if(wcs_arr[i].length > 0){
                    $("#wcsource_qt_id").append("<a href='/shlib/gj/?gj="+wcs_arr[i]+"' target='_blank'>《"+wcs_arr[i]+"》</a>");
                }
            }
        }else{
            $("#wcsource_qt_id").text("无");
        }

        //物产所属分类标签
        var category_qt = "";
        if(data.category_fz != null && data.category_fz!=""){
            category_qt += data.category_fz;
        }
        // if(data.category_qt != null && data.category_qt!=""){
        //     category_qt += data.category_qt;
        // }
        if(category_qt == ""){
            category_qt = "无";
        }
        $("#category_qt_id").append(category_qt);

        //物产相关人物-格式问题 -todo
        if(data.Des_people != "" && data.Des_people != null){
            var ps = data.Des_people.split(";");
            for(var i in ps){
                if(ps[i] != ""){
                    $("#Des_people_id").append("<a href='/shlib/person/?person="+ps[i]+"' target='_blank'>  "+ps[i]+"   </a>");
                }
            }
        }else{
            $("#Des_people_id").append("无");
        }
        
        //物产描述
        if(data.desc != null && data.desc != ""){
            // 物产别名，物产相关人物，物产产地，物产引书
            var strNew = data.desc;
            //别名
            if(data.alternateName != null && data.alternateName != ""){
                var anames = data.alternateName.split(";");
                for(var i in anames){
                    if(anames[i] != "" && strNew.indexOf(anames[i]) >= 0){
                        strNew = strNew.replaceAll(anames[i],
                            "<span style='background-color:#3cc54d' title='别名："+anames[i]+"'>"+anames[i]+"</span>");
                    }
                }
            }
            //Des_people相关人物
            if(data.Des_people != null && data.Des_people != ""){
                var ps = data.Des_people.split(";");
                for(var i in ps){
                    if(ps[i] != "" && strNew.indexOf(ps[i]) >= 0){
                        strNew = strNew.replaceAll(ps[i],"<a href='/shlib/person/?person="+ps[i].trim()+"' target='_blank' style='background-color:#bcd246' title='相关人物："+ps[i]+"'>"+ps[i]+"</a>");
                    }
                }
            }

            //物产产地
            if(data.Des_site != null && data.Des_site != ""){
                var ds = data.Des_site.split(";");
                for(var i in ps){
                    if(ds[i] != "" && strNew.indexOf(ds[i]) >= 0){
                        strNew = strNew.replaceAll(ds[i],"<a href='/shlib/place/?place="+ds[i].trim()+"' target='_blank' style='background-color:#d279e2' title='产地："+ds[i]+"'>"+ds[i]+"</a>");
                    }
                }
            }
            //物产引书
            if(data.Des_cite != null && data.Des_cite != ""){
                var dc = data.Des_cite.split(";");
                for(var i in dc){
                    if(dc[i] != "" && strNew.indexOf(dc[i]) >= 0){
                        strNew = strNew.replaceAll(dc[i],"<span style='background-color:#dc6f45' title='引书："+dc[i]+"'>"+dc[i]+"</span>");
                    }
                }
            }

            //描述信息
            $("#desc_id").append("<h6>方志物产描述:</h6>");
            $("#desc_id").append(strNew);
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
                var href_a = '<a href="javascript:;" data-toggle="m-popover" data-trigger="click" '+
                    ' title="" data-html="true"  '+
                    ' data-content="<div id=\'popover_id\'><a href=\'/shlib/person/?person='+poedata[i].author+'\' target=\'_blank\'>链接上图</a><br/><a href=\'/cbdb/?name='+poedata[i].author+'\' target=\'_blank\'>链接CBDB</a></div>" >'+poedata[i].author+'</a>';
                $("#desc_id").append(href_a);
                $("#desc_id").append("<span style='margin-left:15px;'>《"+poedata[i].title+"》-"+poedata[i].clause+"</span>");
                $("#desc_id").append("<br/>");
            }

            $("[data-toggle='m-popover']").popover();
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
        if(data.longitude != "" && data.latitude != "" 
            && data.place != "" && data.place != null){
            var point = new BMap.Point(data.longitude, data.latitude);
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
        }else{
            //默认地图
            var point = new BMap.Point(102.699, 25.06);
            map.centerAndZoom(point, 8);
        }
    }
});