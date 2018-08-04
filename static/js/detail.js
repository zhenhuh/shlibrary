/**
 * 详细页面JS文件
 */
$(function() {
    //百度地图API功能	
    var map = new BMap.Map("yn_map");
    map.centerAndZoom(new BMap.Point(101.88, 25.7), 8); //经度、维度、精确度（3-19，数字越大，越精确）
    map.enableScrollWheelZoom();
    //加载一个矩形区域地图
    var b = new BMap.Bounds(new BMap.Point(96.037928, 19.802862), //西南角经纬度
        new BMap.Point(107.536239, 29.537083));
    try {
        BMapLib.AreaRestriction.setBounds(map, b);
    } catch (e) {
        alert(e);
    }
});