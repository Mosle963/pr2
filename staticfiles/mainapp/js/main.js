//function to handle showing the option to show more or less
function show_less_more() {
    
    $(".post-body").each(function() {
        var summary = $(this).find(".post-summary")[0];
        var seeMore = $(this).find(".see-more");
        if (summary.scrollHeight > summary.clientHeight) {
            seeMore.show();
        } else {
            seeMore.hide();
        }
    });

    $(".see-more").click(function() {
        console.log('Show more clicked');
        $(this).siblings(".post-summary").hide();
        $(this).siblings(".post-full").show();
        $(this).hide();
        $(this).siblings(".see-less").show();
    });

    $(".see-less").click(function() {
        console.log('Show less clicked');
        $(this).siblings(".post-summary").show();
        $(this).siblings(".post-full").hide();
        $(this).hide();
        $(this).siblings(".see-more").show();
    });
}

   
$(document).ready(function(){
    show_less_more();
    function loadContent(url) {
        if ($("#loading").val()=="true"){ console.log("returned"); return;}
        $("#loading").val("true");

        $.ajax({
            url: url,
            success: function(data) {
            var cur = parseInt($("#page").val(), 10); // Parse the value to an integer
            cur += 1;
            $("#page").val(cur);
            
                $('#posts-container').append(data.content);
                show_less_more();
                $("#loading").val("false");               
                
            },
            error: function() {
                $("#loading").val("false");
                show_less_more();
            }
        });
    
    }

    $(window).scroll(function() {
        if ($(window).scrollTop() + $(window).height() >= $(document).height() - 10) {
            var url = '?page=' + $("#page").val() + '&nav=' + $('.sub-bar.active').attr('href').split('=')[1];
            loadContent(url);
        }
    });

    $('.sub-bar').click(function(e){
            e.preventDefault();
            $('.sub-bar').removeClass('active');
            $(this).addClass('active');
            $('#posts-container').empty(); 
            $("#page").val("1"); // Reset page counter
            var url = $(this).attr('href') + '&page=' + $("#page").val();
            $("#loading").val("false");
            loadContent(url);
        });
    });

document.addEventListener('DOMContentLoaded', function() {
        show_less_more();
    });
    