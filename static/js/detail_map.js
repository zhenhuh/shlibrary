/**
 * 详细页面JS文件
 */
$(function() {
    /**
     * 查询明细数据
     */
    $.ajax({
        url:"/wcstat/",
        type:"post",
        dataType:"json",
        data:{
                wcname:$("#product_name").val()
            },
        success:function(data){
            //展示所有物产的地图
            showProductDataOnMap(data.data);

            //展示明细数据
            showProductDataOnTime(data);
            //时间轴展示数据
            timeClick(data.data);
            
        },
        error:function(data){

        }
    });
    
    /**
     * 展示云南数据
     * @param data 
     */
    function showProductDataOnTime(data){
        for(var i in data.data){
            var tempD = data.data[i];
            var conTemp = '<div class="m-timeline-2__item"><span class="m-timeline-2__item-time">'+
                            tempD.time_w + '</span>'+
                '<div class="m-timeline-2__item-cricle" data-index="'+i+'"><i class="fa fa-genderless m--font-brand"></i></div>'+
                '<div class="m-timeline-2__item-text  m--padding-top-5">'+
                    '<span>'+tempD.time_c+'在'+tempD.source+'中记载</span>'+
                    '<span>出自:' +((tempD.area_record==null || tempD.area_record == "")?"不详":tempD.area_record)+'</span>'+
                    '<span>所属分类为:'+tempD.category+'</span>'+
                '</div></div>';
            $("#wc_name_details").append(conTemp);
        }
        $(".m-timeline-2__item-cricle").first().addClass("active");
    }
});

    /**
     * 展示云南数据
     * @param data 
     */
    function showProductDataOnMap(data){
        var map = new BMap.Map("yn_map_detail");
        var point = new BMap.Point(101.88, 25.7);
        map.centerAndZoom(point, 8);
        map.enableScrollWheelZoom();

        for(var i in data){
            var tempD = data[i].map_location;
            var pt = new BMap.Point(tempD.longitude,tempD.latitude);
            var marker = new BMap.Marker(pt);  // 创建标注
            map.addOverlay(marker);               // 将标注添加到地图中
            marker.setAnimation(BMAP_ANIMATION_BOUNCE); //跳动的动画

            var opts = {
                position :pt,    // 指定文本标注所在的地理位置
                offset   : new BMap.Size(20, -10)    //设置文本偏移量
            }
            var label = new BMap.Label(tempD.place,opts);
            marker.setLabel(label);
            if(i == 0){
                map.centerAndZoom(pt, 8);
                map.enableScrollWheelZoom();
            }
        }
    }