$(document).ready(function () {

    // loading external files
    var product_template_url= '/static/store/mustache_templates/product_template.mst';
    var template_cache = {};
    $.get('/static/store/mustache_templates/product_template.mst', function(template) {
                    template_cache[product_template_url] = template;
                  });

    // function definitions

    var mustachify_product = function(product){
        product.fields.title_short = product.fields.title.substr(0, 25);
        if(product.fields.stock!="In Stock"){
            product.fields.no_stock = true;
        }
        return product;
    }

    var populate_products = function(response){
        var products = response.products;
        var p_container = $("#product-container");
        p_container.html('');
        $.each(products, function(index, product){
              var product_m = mustachify_product(product);
              if(template_cache[product_template_url] == undefined){
                $.get('/static/store/mustache_templates/product_template.mst', function(template) {
                    var rendered = Mustache.render(template, {'product': product_m});
                    p_container.append(rendered);
                    template_cache[product_template_url] = template;
                  });
              }else{
                    var template = template_cache[product_template_url];
                    var rendered = Mustache.render(template, {'product': product_m});
                    p_container.append(rendered);
              }

        });
        var page_info = response.page_info
        $("#page-next").data('url', page_info.next_page);
        $("#page-next").attr('href', page_info.next_page);
        $("#page-previous").data('url', page_info.previous_page);
        $("#page-previous").attr('href', page_info.previous_page);
    }

    var populate_filter_menu = function(filter_options){
        var category_options = filter_options['categories'];
        var brand_options = filter_options['brands']

        var category_menu = $("#filter-category-menu").find('.panel-body');
        $.each(category_options, function(index, category_option){
            if(category_option.category){
                var category_option_element_str = '<span class="filter-option"><input data-type="category" hidden type="checkbox" value="__catname__" id="__category_index__"><label class="label label-default" for="__category_index__">__catname__</label></span>';
                category_option_element_str = category_option_element_str.replace(/__catname__/g, category_option.category);
                category_option_element_str = category_option_element_str.replace(/__category_index__/g, "category_"+index);
                var category_option_element =  $(category_option_element_str);
                category_menu.append(category_option_element);
            }
        });

        var brand_menu = $("#filter-brand-menu").find('.panel-body');
        $.each(brand_options, function(index, brand_option){
            if(brand_option.brand){
                var brand_option_element_str = '<span class="filter-option"><input data-type="brand" hidden type="checkbox" value="__brandname__" id="__brand_index__"><label class="label label-default" for="__brand_index__">__brandname__</label></span>';
                brand_option_element_str = brand_option_element_str.replace(/__brandname__/g, brand_option.brand);
                brand_option_element_str = brand_option_element_str.replace(/__brand_index__/g, "brand_"+index);
                var brand_option_element = $(brand_option_element_str);
                brand_menu.append(brand_option_element);
            }
        });


    }

    var do_get_request = function(request_url, handler){
        var json_request = $.ajax({
            method: "GET",
            url: request_url,
            dataType: "json"
        });
        json_request.done(handler);
    }


    // observers

    $("#search-bar").keyup(function(ev){
        var el = $(ev.target);
        var search_term = el.val()
        if(search_term.length > 2){
            var request_url = "/store/product/search/?q="+search_term
            do_get_request(request_url, populate_products);
         }
    });

    $(".page-btn").click(function(ev){
        ev.preventDefault();
        el = $(ev.target)
        page_url = el.data('url');
        do_get_request(page_url, populate_products);
        $("html, body").animate({ scrollTop: 0 }, "slow");
    });

    $('#filter-menu').on('click', ':checkbox', function (ev) {
        var el = $(ev.target);
        el.siblings('label').toggleClass('label-warning');
        checked_boxes = $(':checkbox:checked')
        base_url = "/store/product/?";
        for(var i=0; i< checked_boxes.length; i++){
            var checkbox = $(checked_boxes[i]);
            if(checkbox.data('type') == "price"){
                price_arr = checkbox.val().split("-");
                base_url += "price_range_low="+price_arr[0]+"&price_range_high="+price_arr[1]+"&";
            }else{
                base_url += checkbox.data('type')+"="+checkbox.val()+"&";
            }
        }
        do_get_request(encodeURI(base_url), populate_products);
        console.log(base_url);
    });

    $('#search-bar').on('hide.bs.collapse', function (e) {
        $("#filter-menu").collapse('hide');
    });

    // init here
    do_get_request("/store/product/", populate_products);
    do_get_request("/store/filter_option/", populate_filter_menu);

});