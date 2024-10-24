//function to handle user refreshing the status
function refreshStatus(post_id) {
    const refreshButton = document.getElementById('refreshbtn'+post_id);
    const refreshIcon = document.getElementById('refreshicon'+post_id);
    var refresh_url = $("#refresh_url").val();
    
    refreshIcon.classList.add('fa-spin'); // Add spinning class
    refreshButton.setAttribute('disabled','true')
    fetch(refresh_url.replace("0", post_id))
        .then(response => response.text())
        .then(data => {
            
            document.getElementById('refresh'+post_id).textContent = data;
            document.getElementById('refresh'+post_id).setAttribute('data-status', data);
            if(data!='Processing..')
                {
                   refreshButton.setAttribute('hidden','true')
                   refreshIcon.setAttribute('hidden','true')  
                }
            else{refreshIcon.classList.remove('fa-spin');            
                refreshButton.removeAttribute('disabled');
            }
        })
        .catch(error => {
            console.error('Error fetching status:', error);
            alert("Error fetching status.");
            refreshIcon.classList.remove('fa-spin');
            refreshButton.removeAttribute('disabled');
            
        });
}