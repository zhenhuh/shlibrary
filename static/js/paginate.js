$.extend({

    /**
     * 分页回显
     * 
     */
    callbackPageinfo:function(data){
        var $obj = $(".dataTables_wrapper");
        //当前页码信息
        $obj.find("#page_data_info_id").text("共"+data.count+"条，当前页面从 "+(data.first_index+1)+" 条至 "+(data.last_index+1)+" 条");

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
            //解除所有绑定事件
            $(ele).unbind();
            
            $(ele).click(function(){
                //切换页面样式
                $obj.find(".page_num").removeClass("active");
                $(ele).addClass("active");
                //获取页码查询数据
                var click_page = $(this).find(".page-link").text().trim();
                if(click_page - advancedPageData.current_page != 0){
                    advancedPageData.current_page = click_page;
                    searchByPageIndex(advancedPageData);
                }
            });
        });

        //下一页事件
        //解除所有绑定事件
        $obj.find("#m_table_1_next").unbind();
        $obj.find("#m_table_1_next").click(function(){
            if(!data.page_next){
                return;
            }
            //获取当前页码
            var currentPage = $obj.find(".page_num.active .page-link").text().trim();
            currentPage = parseInt(currentPage,10);
            //获取当前展示的最后一个页码
            var lastPage = $obj.find(".page_num").last().find(".page-link").text().trim();
            lastPage = parseInt(lastPage,10);
            //如果当前页是最后一个页码，则往后移动一个
            if(currentPage - lastPage == 0){
                $obj.find(".page_num").each(function(index,ele){
                    var pageNum = $(ele).find(".page-link").text().trim();
                    pageNum = parseInt(pageNum,10);
                    $(ele).find(".page-link").text(pageNum+1);
                    $(ele).find(".page-link").attr("data-dt-idx",(pageNum+1));
                });
                $obj.find(".page_num").removeClass("active");
                $obj.find(".page_num").last().addClass("active");
            }else{
                $obj.find(".page_num").removeClass("active");
                $obj.find(".page-link[data-dt-idx='"+(currentPage+1)+"']").parent().addClass("active");
            }
            //查询数据
            advancedPageData.current_page = currentPage + 1;
            searchByPageIndex(advancedPageData);
        });
        //跳转到最后一页事件
        $obj.find("#m_table_1_last").unbind();
        $obj.find("#m_table_1_last").click(function(){
            if(!data.page_next){
                return;
            }
            
            //获取当前展示的最后一个页码
            var lastPage = $obj.find(".page_num").last().find(".page-link").text().trim();
            lastPage = parseInt(lastPage,10);
            
            var maxPage = parseInt(data.page_count,10);
        
            //如果最后一个页码即最后一页，则不需要改变页码数字,直接跳到最后一页，否则转换页码
            if(maxPage - lastPage == 0){
                $obj.find(".page_num").removeClass("active");
                $obj.find(".page_num").last().addClass("active");
            }else{
                $obj.find(".page_num").each(function(index,ele){
                    $(ele).find(".page-link").text(maxPage-4+index);
                    $(ele).find(".page-link").attr("data-dt-idx",(maxPage-4+index));
                });
                $obj.find(".page_num").removeClass("active");
                $obj.find(".page_num").last().addClass("active");
            }
            //查询数据
            advancedPageData.current_page = maxPage;
            searchByPageIndex(advancedPageData);
        });

        //跳转到第一页事件
        $obj.find("#m_table_1_first").unbind();
        $obj.find("#m_table_1_first").click(function(){
            if(!data.page_prev){
                return;
            }

            //获取当前展示的第一个页码
            var firstPage = $obj.find(".page_num").first().find(".page-link").text().trim();
            firstPage = parseInt(firstPage,10);
        
            //如果第一个页码即第一页，则不需要改变页码数字,直接跳到第一页，否则转换页码
            if(firstPage - 1 == 0){
                $obj.find(".page_num").removeClass("active");
                $obj.find(".page_num").first().addClass("active");
            }else{
                $obj.find(".page_num").each(function(index,ele){
                    $(ele).find(".page-link").text(1+index);
                    $(ele).find(".page-link").attr("data-dt-idx",(1+index));
                });
                $obj.find(".page_num").removeClass("active");
                $obj.find(".page_num").first().addClass("active");
            }
            //查询数据
            advancedPageData.current_page = 1;
            searchByPageIndex(advancedPageData);
        });

        //上一页事件
        $obj.find("#m_table_1_previous").unbind();
        $obj.find("#m_table_1_previous").click(function(){
            if(!data.page_prev){
                return;
            }
            //获取当前页码
            var currentPage = $obj.find(".page_num.active .page-link").text().trim();
            currentPage = parseInt(currentPage,10);
            //获取当前展示的第一个页码
            var firstPage = $obj.find(".page_num").first().find(".page-link").text().trim();
            firstPage = parseInt(firstPage,10);
            //如果当前页是第一个页码，则往前移动一个
            if(currentPage - firstPage == 0){
                $obj.find(".page_num").each(function(index,ele){
                    var pageNum = $(ele).find(".page-link").text().trim();
                    pageNum = parseInt(pageNum,10);
                    $(ele).find(".page-link").text(pageNum-1);
                    $(ele).find(".page-link").attr("data-dt-idx",(pageNum-1));
                });
                $obj.find(".page_num").removeClass("active");
                $obj.find(".page_num").last().addClass("active");
            }else{
                $obj.find(".page_num").removeClass("active");
                $obj.find(".page-link[data-dt-idx='"+(currentPage-1)+"']").parent().addClass("active");
            }
            //查询数据
            advancedPageData.current_page = currentPage - 1;
            searchByPageIndex(advancedPageData);
        });
        
        // first_index
        // last_index
        // page_count
        // current_page
    }
});