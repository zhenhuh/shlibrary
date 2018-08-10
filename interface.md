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
> * name模糊匹配
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
        {
            "uid": "35387",
            "product_name": "云台松子",
            "wcsource": "宜良县志　",
            "temporal": "民国１０年(1921)",
            "gjsource": ""
        },
        {
            "uid": "64689",
            "product_name": "大松子",
            "wcsource": "",
            "temporal": "",
            "gjsource": ""
        },
        {
            "uid": "10752",
            "product_name": "松子",
            "wcsource": "云南通志",
            "temporal": "明.隆庆6年(1572)",
            "gjsource": ""
        }
    ]
}
```
> 返回值说明  
> count : 搜索结果总数  
> data : 数据列表(10条)  
> 按物产名排序
> 查不到数据返回 {"count":0, "data":[]}

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
    {
        "uid": "7030",
        "product_name": "冷水谷",
        "wcsource": "云南通志稿",
        "temporal": "清·光绪27(1901)",
        "describe": "通海县续志稻之类甚多而宜于冷水谷其谷最耐寒晚熟通海湖风早寒故宜然三四月遂生虫不堪贮仓",
        "gjsource": "通海县续志"
    },
    {
        "uid": "43040",
        "product_name": "浮尘子",
        "wcsource": "宣威县志",
        "temporal": "民国23年(1934)",
        "describe": "稻之害虫形如小蝉或绿色或浓褐色嘴作管状入稻茎叶中吸收汁液稻即枯萎",
        "gjsource": ""
    },
    {
        "uid": "1673",
        "product_name": "麒麟竭",
        "wcsource": "滇志",
        "temporal": "明天启5年(1625)",
        "describe": "木高数丈婆娑崝菁叶似樱桃有三角脂从木中流出如胶结赤如血色又曰血竭",
        "gjsource": ""
    }
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

# 4. 首字母点击返回数据接口

##  - 入参说明
* letter : 点击的首字母
* current_page : 结果当前所在页面

> 限制条件  
> letter参数大写
> letter和current_page必须有值, current_page从1开始

`Sample URL:`
http://localhost:2345/RESTfulWS/JL/wc/certainL?letter=A&current_page=1

## - 返回格式
```
{
  "count": 72,
  "data": [
    {
      "wcname": "艾"
    },
    {
      "wcname": "安颠榖"
    },
    {
      "wcname": "矮足鸡冠"
    }
  ]
}
```

> 返回值说明  
> data里面15个条目, 并且去重

# 5. 分类标签接口

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

# 6. 分类标签点击返回数据接口

##  - 入参说明
* category : 点击的标签
* current_page : 结果当前所在页面

> 限制条件  
> category和current_page必须有值, current_page从1开始

`Sample URL:`
http://localhost:2345/RESTfulWS/JL/wc/certainClass?category=花之属&current_page=1

## - 返回格式
```
{
  "count": 1769,
  "data": [
    {
      "wcname": "松子"
    },
    {
      "wcname": "邓花"
    },
    {
      "wcname": "嘉莲"
    }
  ]
}
```

> 返回值说明  
> data里面15个条目, 并且去重

# 7. 云南地区接口

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

# 8. 云南地区点击返回数据接口

##  - 入参说明
* region : 点击的地区
* current_page : 结果当前所在页面

> 限制条件  
> region和current_page必须有值, current_page从1开始

`Sample URL:`
http://localhost:2345/RESTfulWS/JL/wc/certainRegion?region=云南府&current_page=1

## - 返回格式
```
{
  "count": 5624,
  "data": [
    {
      "wcname": "松子"
    },
    {
      "wcname": "邓花"
    },
    {
      "wcname": "嘉莲"
    }
  ]
}
```

> 返回值说明  
> data里面15个条目, 并且去重

# 9. 物产详细信息接口

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

# 10. 其他古籍详细信息接口

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

# 11. 方志物产详细信息接口

##  - 入参说明
* fzname : 方志名称
* wtime : 西历年份

> 限制条件  
> fzname和wtime必须有值

`Sample URL:`
http://localhost:2345/RESTfulWS/JL/jtwc/lyfzDetail?fzname=云南图经志书&wtime=1455

## - 返回格式
```
{
    "id": "1",
    "bookname": "云南图经志书",
    "author": "（明）郑颙修；(明)陈文纂",
    "author1": "",
    "author2": "",
    "writer_x": "（明）郑颙",
    "writer_z": "(明)陈文",
    "column": "十卷",
    "author_xz": "",
    "abs": "",
    "publish_p": "",
    "publish_a": "",
    "time_b": "",
    "time_k": "明景泰六年",
    "time_c": "",
    "type": "通志",
    "library1": "国家图书馆",
    "library2": "上海图书馆",
    "library3": "云南省图书馆",
    "url": "",
    "database": "",
    "class_number": "",
    "area": "云南",
    "longitude": "102.73",
    "latitude": "25.04",
    "dynasty": "明",
    "year_c": "景泰六年",
    "year_w": "1455",
    "catelog_u": "有",
    "category_y": "有",
    "category_z": "有",
    "category_t": "有"
}
```

> 返回值说明  
> (None)

# 12. 地图经纬度接口

##  - 入参说明
* place : 地图地点

> 限制条件  
> place对应的是物产详细信息里的 `mapPlace`, 去掉两端空格

`Sample URL:`
http://localhost:2345/RESTfulWS/JL/jtwc/lyplace?place=六顺县

## - 返回格式
```
{
  "place": "六顺县",
  "longitude": "100.88333333333334",
  "latitude": "22.733333333333334"
}
```

> 返回值说明  
> 地点名和经纬度信息
> 经纬度信息是符合BaiduMap的经纬度格式

# 13. 物产统计接口

##  - 入参说明
* wcname : 物产名称

> 限制条件  
> wcname必须有值, 精确查询

`Sample URL:`
http://localhost:2345/RESTfulWS/JL/wc/tjwc?wcname=松子

## - 返回格式
```
{
  "count": 121,
  "data": [
    {
        "wc_id": "1",
        "wc_name": "松子",
        "source": "云南图经志书",
        "time_c": "明景泰6年",
        "time_w": "1455",
        "category": "土产",
        "area_record": "云南府",
        "area_map": "云南府"
    },
    {
        "wc_id": "111",
        "wc_name": "松子",
        "source": "云南志",
        "time_c": "明正德5年",
        "time_w": "1510",
        "category": "土产",
        "area_record": "云南府",
        "area_map": "云南府"
    }
}
```

> 返回值说明  
> (None)

# 14. 方志统计接口

##  - 入参说明
* (None)

> 限制条件  
> (None)

`Sample URL:`
http://localhost:2345/RESTfulWS/JL/jtwc/allFZ

## - 返回格式
```
[
    {
        "id": "1",
        "bookname": "云南图经志书",
        "type": "通志",
        "area": "云南",
        "longitude": "102.73",
        "latitude": "25.04"
    },
    {
        "id": "2",
        "bookname": "云南志",
        "type": "通志",
        "area": "云南",
        "longitude": "102.73",
        "latitude": "25.04"
    }
]
```

> 返回值说明  
> (None)

# 15. 方志中物产数量统计接口

##  - 入参说明
* fzname : 方志名称

> 限制条件  
> fzname必须有值

`Sample URL:`
http://localhost:2345/RESTfulWS/JL/jtwc/wcTJ?fzname=云南图经志书

## - 返回格式
```
{
  "wc_count": 105
}
```

> 返回值说明  
> (None)

# 0. TODO接口

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