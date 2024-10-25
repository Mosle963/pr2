
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
            
            const followersElement = document.getElementById('followers_number');
            const followersText = followersElement.textContent;          
            const followersNumber = parseInt(followersText.match(/\d+/)[0], 10);
            const followIcon = document.getElementById('star');
            followIcon.classList.toggle('bi-star');
            followIcon.classList.toggle('bi-star-fill');
            const followbtn = document.getElementById('followbtn');
            title = followbtn.getAttribute('title');
            if(title=='follow')
                {
                    followbtn.setAttribute('title','unfollow');
                    const updatedFollowersNumber = followersNumber + 1;
                    followersElement.textContent = `Number of Followers : ${updatedFollowersNumber}`;

                }
            else{
                followbtn.setAttribute('title','follow')
                const updatedFollowersNumber = followersNumber - 1;
                followersElement.textContent = `Number of Followers : ${updatedFollowersNumber}`;

            }
                    }
    });
}

