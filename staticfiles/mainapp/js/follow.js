
//function to handle the follow
function follow(followee_id) 
{
    var follow_url = $("#follow_url").val();
    var csrf_token = $("#csrf_token").val();
    
    fetch(follow_url.replace(0, followee_id), {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const followIcon = document.getElementById('star');
            followIcon.classList.toggle('bi-star');
            followIcon.classList.toggle('bi-star-fill');
            const followbtn = document.getElementById('followbtn');
            title = followbtn.getAttribute('title');
            if(title=='follow')
                {
                    followbtn.setAttribute('title','unfollow');
                }
            else{
                followbtn.setAttribute('title','follow')
            }
        }
    });
}

