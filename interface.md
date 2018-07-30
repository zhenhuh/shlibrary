**-- 说明 --**  
**数据服务端口 : 2345**  
**返回数据如不做特殊要求均为json格式**  
**所有限制条件如不做特殊说明, 都在后台处理, 不在数据服务处理**

# 1. 搜索接口

##  - 入参说明
### 高级搜索
* name : 物产名称
* year_start : 开始时间
* year_end : 结束时间
* source_lc : 来源志书
* yn_region : 云南行政区域
* current_page : 结果当前所在页面

### 普通搜索
* name : 物产名称或来源支书
* current_page : 结果当前所在页面

> 限制条件  
> * current_page必须有值, 从1开始, 最大不超过页面数  
> * 其他字段必须要有一个字段有值

`Sample URL:`
http://localhost:2345/search/?name=松子&current_page=1&source_lc=云南志书

## - 返回格式
```
{
    "count":"107",
    "data":[
        {"uid":"1","product_name":"松子","temporal":"明景泰6年(1455)","desc":"树皮无龙鳞而稍光滑枝"},
        {"uid":"2","product_name":"松子","temporal":"明正德5年(1510)","desc":""},
        {"uid":"3","product_name":"松子","temporal":"明正德5年(1510)","desc":""}
    ]
}
```
> 返回值说明  
> count : 搜索结果总数
> data : 数据列表(10条)

# 2. 首页随机展示接口

##  - 入参说明
* (None)

> 限制条件  
> (None)

`Sample URL:`
http://localhost:2345/random_list

## - 返回格式
```
[
    {"uid":"1","product_name":"松子","temporal":"明景泰6年(1455)","desc":"树皮无龙鳞而稍光滑枝"},
    {"uid":"2","product_name":"松子","temporal":"明正德5年(1510)","desc":""},
    {"uid":"3","product_name":"松子","temporal":"明正德5年(1510)","desc":""}
]
```

> 返回值说明  
> 10条随机数据

# 3. TODO接口

##  - 入参说明
* TODO

> 限制条件  
> TODO

`Sample URL:`
http://localhost:2345/

## - 返回格式
```
TODO
```

> 返回值说明  
> TODO