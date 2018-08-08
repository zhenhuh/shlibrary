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
> * 其他字段必须要有一个字段有值, 没有值默认-1
> * current_page超过最大页面数, data字段为 []

`Sample URL:`
http://localhost:2345/RESTfulWS/JL/wc/gjwc/?name=松子&current_page=1&year_start=-1&year_end=-1&source_lc=云南志书&yn_region=-1

## - 返回格式
```
{
    "count":107,
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
> 按物产名排序

# 2. 首页随机展示接口

##  - 入参说明
* (None)

> 限制条件  
> (None)

`Sample URL:`
http://localhost:2345/RESTfulWS/JL/wc/list

## - 返回格式
```
[
    {"uid":"1","product_name":"松子","wcsource": "云南图经志书","temporal": "明景泰6年(1455)","gjsource": ""},
    {"uid":"2","product_name":"松子","wcsource": "云南志","temporal": "明正德5年(1510)","gjsource": ""},
    {"uid":"3","product_name":"松子","wcsource": "云南志","temporal": "明正德5年(1510)","gjsource": ""}
]
```

> 返回值说明  
> 10条随机数据

# 3. 首字母查询接口

##  - 入参说明
* (None)

> 限制条件  
> (None)

`Sample URL:`
http://localhost:2345/RESTfulWS/JL/wc/firstletter

## - 返回格式
```
[
    {"letter":"A","count":100},
    {"letter":"B","count":200}
]
```

> 返回值说明  
> (None)

# 4. 分类标签接口

##  - 入参说明
* (None)

> 限制条件  
> (None)

`Sample URL:`
http://localhost:2345/RESTfulWS/JL/wc/taxonomy

## - 返回格式
```
[
    {"taxonomy":"土产","count":100},
    {"taxonomy":"物产","count":200}
]
```

> 返回值说明  
> (None)

# 5. 云南地区接口

##  - 入参说明
* (None)

> 限制条件  
> (None)

`Sample URL:`
http://localhost:2345/RESTfulWS/JL/wc/ynregion

## - 返回格式
```
[
    {"region":"云南府","count":100},
    {"region":"建水州","count":200}
]
```

> 返回值说明  
> (None)

# 6. 物产详细信息接口

##  - 入参说明
* id : 物产条目id

> 限制条件  
> 必须要有id参数

`Sample URL:`
http://localhost:2345/RESTfulWS/JL/jtwc/detail/?id=1

## - 返回格式
```
{
    "uid": "1",
    "product_name": "松子",
    "wcsource_fz": "云南图经志书",
    "wcsource_qt": "证类本草;滇游记;云南掌故;宁蒗见闻录;",
    "temporal": "明景泰6年(1455)",
    "category_fz": "土产",
    "category_qt": "花之属",
    "alternateName": "",
    "Des_people": "",
    "Des_site": "",
    "Des_cite": "",
    "mapPlace": "云南府",
    "recordPlace": "云南府",
    "desc": "树皮无龙鳞而稍光滑枝上结松毬大如茶瓯其中含宝有二三百粒者"
}
```

> 返回值说明  
> product_name没有空格

# 7. 其他古籍详细信息接口

##  - 入参说明
* wcname : 物产名称
* gjname : 古籍列表

> 限制条件  
> wcname 和 gjname 都要有值

`Sample URL:`
http://localhost:2345/RESTfulWS/JL/jtwc/gjdetail/wcname=松子&gjname=证类本草;滇游记;

## - 返回格式
```
[
    {
        "uid": "15713",
        "product_name": "松子",
        "gj_category": "果之属-",
        "gj_sourceClassify": "",
        "gjsource": "《证类本草》",
        "gjcol": "",
        "gjpage": "卷23",
        "gjdesc": "《海药》云：云南松子似巴豆，其体不厚，多食发热毒。松子味甘美，大温无毒，主诸风，温肠胃，久服轻身，延年不老",
        "gjdesc_name": "",
        "gjdesc_area": "云南",
        "gjdesc_cite": "《海药》",
        "gjdesc_people": ""
    },
    {
        "uid": "15718",
        "product_name": "松子",
        "gj_category": "果之属-",
        "gj_sourceClassify": "",
        "gjsource": "《滇游记》",
        "gjcol": "",
        "gjpage": "第7页",
        "gjdesc": "大和县，......榛松皆不下辽东，但味淡少逊耳。",
        "gjdesc_name": "",
        "gjdesc_area": "",
        "gjdesc_cite": "",
        "gjdesc_people": ""
    }
]
```

> 返回值说明  
> 如果参数内容错误，返回空列表  
> 其他古籍的物产描述的信息一起返回

# 8. TODO接口

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