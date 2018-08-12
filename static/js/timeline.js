/**
 * 点击播放
 */
function timeClick(data) {
    var timer,
        index,//定义时间点选中状态时的索引
        $timeParent=$(".m-timeline-2"),
        $timeChild=$(".m-timeline-2 .m-timeline-2__item-cricle"),
        lenCount=$timeChild.length; 
    
    //点击播放时间轴事件
    $("#wc_detail_body_id").on("click",".time-play",function () {
        $(this).removeClass("time-play").addClass("time-pause");
        index=Number($timeParent.find(".m-timeline-2__item-cricle.active").attr("data-index"));//将字符串强制转换为数字类型
        
        timer=setInterval(function () {
            //判断当前索引的位置，如果在最后一位则从第一个时间点开始，反之则按顺序播放
            if(lenCount==index+1){
                $timeParent.find(".m-timeline-2__item-cricle:eq('"+lenCount+"')").removeClass("active");
                $timeParent.find(".m-timeline-2__item-cricle:eq(0)").addClass("active");
            }else{
                $(".m-timeline-2__item-cricle.active").parent().next().find(".m-timeline-2__item-cricle").addClass("active").siblings().removeClass("active");
                $(".m-timeline-2__item-cricle.active").first().removeClass("active")
            }
            var timeStr = $(".m-timeline-2__item-cricle.active").parent().find("span").first().text().trim();
        
            if(timeStr != null && timeStr != ""){
                var timeInt = parseInt(timeStr,10);
                if(timeInt){
                    setMapData(data,timeInt);
                }
            }

            $timeChild.each(function () {
                if($(this).hasClass("active")){
                    index=Number($(this).attr("data-index"));//字符串转换为数字类型，索引从0开始
                }
            });
        },2000)
    });
    //点击暂停按钮事件
    $("#wc_detail_body_id").on("click",".time-pause",function () {
        $(this).removeClass("time-pause").addClass("time-play");
        clearInterval(timer);//清除定时器
    });
    //点击某个时间点时触发事件
    $timeChild.not(":first-child").click(function () {
        var index=$(this).data("index");
        $(".m-timeline-2__item-cricle").removeClass("active");
        $(this).addClass("active");
        clearInterval(timer);//清除定时器
        var timeStr = $(this).parent().find("span").first().text().trim();
        
        if(timeStr != null && timeStr != ""){
            var timeInt = parseInt(timeStr,10);
            if(timeInt){
                setMapData(data,timeInt);
            }
        }
    })
}

/**
 * 根据时间查询数据
 */
function getDataByTime(data,time){
    var rtData = [];
    for(var i in data){
        if(time == data[i].time_w){
            rtData.push(data[i]);
        }
    }
    return rtData;
}

/**
 * 调用地图加载
 */
function setMapData(data,time){
    var rtData = getDataByTime(data,time);
    showProductDataOnMap(rtData);
}