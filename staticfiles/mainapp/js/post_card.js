function change_status(new_status, checker_id, post_id) {
    var update_url = $("#update_url").val();
    var csrf_token = $("#csrf_token").val();
    fetch(update_url.replace("0", post_id), {
        method: 'POST',
        body: JSON.stringify({ 'new_status': new_status, 'checker_id': checker_id }),
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrf_token
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {

            var statusHtml = 'Truth-O-meter: <strong class="text-dark">'+data.new_status+'</strong>';
            if (data.checker_name) {
                statusHtml += ' by <a id="checker-link" href="'+data.checker_url+'">'+data.checker_name+'</a>';
            }
            idd = "poststatue"+post_id;
            document.getElementById(idd).innerHTML = statusHtml;
            //  $("#post-statue-" + post_id).html(statusHtml); // Directly update HTML content
        } else {
            alert("Failed to alter status.");
        }
    });
}

    
function deletePost(post_id) {
    var delete_url = $("#delete_url").val();
    var csrf_token = $("#csrf_token").val();
    fetch(delete_url.replace("0", post_id), {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrf_token
        }
    })
    .then(response => response.json())    
    .then(data => {
            if (data.success) {
                idd = "post-card-"+post_id
                document.getElementById(idd).remove();  // Remove the post card
            } else {
                alert("Failed to delete post.");
            }
        });
}

function show_less_more() {
    
    console.log("called");
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

$(document).ready(function() {
    show_less_more();
});
