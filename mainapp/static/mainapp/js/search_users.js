//function to show the suggetions in realted to query in search box
function showSuggestions(users) {
    const suggestionsBox = document.getElementById('suggestions-box');
    suggestionsBox.innerHTML = '';
    users.forEach(user => {
        const suggestionItem = document.createElement('div');
        suggestionItem.classList.add('suggestion-item');
        
        // Make the suggestion a clickable link
        const link = document.createElement('a');
        link.href = user.account_url;
        link.textContent = user.username;
        link.classList.add('d-block'); // Makes the entire item clickable
        
        suggestionItem.appendChild(link);
        suggestionsBox.appendChild(suggestionItem);
    });
}


//function to get the query search 
function searchUsers(query) {
    if (query.length > 0) {
        var url = $("#autocomplete_users").val();
        fetch(url+"?query="+query)
            .then(response => response.json())
            .then(data => {
                showSuggestions(data);
            })
            .catch(error => {
                console.error('Error fetching user suggestions:', error);
            });
        } 
    else {document.getElementById('suggestions-box').innerHTML = '';}
}