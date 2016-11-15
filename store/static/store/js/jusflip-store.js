$(document).ready(function () {

    var product_template_url= '/static/store/mustache_templates/product_template.mst';
    var template_cache = {};
    $.get('/static/store/mustache_templates/product_template.mst', function(template) {
                    template_cache[product_template_url] = template;
                  });
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
    var json_request = $.ajax({
        method: "GET",
        url: "/store/product/",
        dataType: "json"
    });
    json_request.done(populate_products);


    $("#search-bar").keyup(function(ev){
        var el = $(ev.target);
        var search_term = el.val()
        if(search_term.length > 3){
            var json_request = $.ajax({
                    method: "GET",
                    url: "/store/product/search/?q="+search_term,
                    dataType: "json"
               });
            json_request.done(populate_products);
         }
    });

    $(".page-btn").click(function(ev){
        ev.preventDefault();
        el = $(ev.target)
        page_url = el.data('url');
        var json_request = $.ajax({
        method: "GET",
        url: page_url,
        dataType: "json"
    });
    json_request.done(populate_products);
     $("html, body").animate({ scrollTop: 0 }, "slow");
    });


});