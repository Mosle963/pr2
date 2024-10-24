//function to delete post
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
