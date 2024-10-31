//function to handle trusted user changing post status
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
            
            var statusHtml = 'Truth-O-meter: ';
            statusHtml+='<strong id = ';
            statusHtml+='"refresh'+post_id+'" ';
            statusHtml+='class="mystatus" ';
            statusHtml+='data-status="'+data.new_status+'"';
            statusHtml+='>'+data.new_status+'</strong>';
            
            
            if (data.checker_name) {
                statusHtml += ' by <a id="checker-link" href="'+data.checker_url+'">'+data.checker_name+'</a>';
            }
            idd = "poststatue"+post_id;
            document.getElementById(idd).innerHTML = statusHtml;
        } else {
            alert("Failed to alter status.");
        }
    });
}
