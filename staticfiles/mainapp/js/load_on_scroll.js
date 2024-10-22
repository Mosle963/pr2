   
$(document).ready(function(){
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