$.extend({
    /**
     * 分页回显
     * 
     */
    callbackPageinfo:function(data){
        var $obj = $(".dataTables_wrapper");
        //页码数
        var pagenum = 5;
        //当前分页数据信息

        //如果有下一页
        if(data.page_next){
            $obj.find("#m_table_1_next").removeClass("disabled");
            $obj.find("#m_table_1_last").removeClass("disabled");
        }else{
            $obj.find("#m_table_1_next").addClass("disabled");
            $obj.find("#m_table_1_last").addClass("disabled");
        }
        //如果有上一页
        if(data.page_prev){
            $obj.find("#m_table_1_first").removeClass("disabled");
            $obj.find("#m_table_1_previous").removeClass("disabled");
        }else{
            $obj.find("#m_table_1_first").addClass("disabled");
            $obj.find("#m_table_1_previous").addClass("disabled");
        }

        //页码点击事件
        $obj.find(".page_num").each(function(index,ele){
            $(ele).click(function(){
                var click_page = $(this).find(".page-link").text();

                alert(click_page.trim());
            });
        });

        //下一页事件
        $obj.find("#m_table_1_next").click(function(){

        });
        //跳转到最后一页事件
        $obj.find("#m_table_1_last").click(function(){

        });

        //跳转到第一页事件
        $obj.find("#m_table_1_first").click(function(){

        });
        //上一页事件
        $obj.find("#m_table_1_previous").click(function(){

        });
        
        // first_index
        // last_index
        // page_count
        // current_page
    }
});