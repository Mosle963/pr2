//function to show message after a post-create 
function showFlashMessage(message, type) {
    var alertDiv = $('<div class="alert alert-' + type + '" role="alert">' + message + '</div>');
    $('#postForm').prepend(alertDiv);
    setTimeout(function() {
        alertDiv.fadeOut(function() {
            $(this).remove();
        });
    }, 4000);
}



function create_post(form,event){
    event.preventDefault();  //preventong sumbmitting through post
    
    //change the button content while posting
    var submitButton = $(form).find('button[type="submit"]');
    var originalButtonText = submitButton.text();
    submitButton.text('Posting...').prop('disabled', true);

    
    //creating a ajax post request
    $.ajax({
        type: 'POST',
        url: form.action,
        data: $(form).serialize(),
        success: function(response) {
                    if (response.success) {
                        // Handle success response (e.g., refresh posts list, show success message)
                        $('#all_posts_nav').click();
                        showFlashMessage("Post created successfully!", "success");
                        $('#postForm')[0].reset();  // Reset the form after successful submission
                        show_less_more();
                    } 
                    else {
                        // Inspect the error object and handle errors
                        var errorMsg = response.errors?.post_text?.[0]?.message ?? "Unknown error occurred"; // Optional chaining to safely access the nested properties
                        showFlashMessage(errorMsg, "danger");
                    }
            // Reset button state
            submitButton.text(originalButtonText).prop('disabled', false);  
        },
        error: function(xhr, status, error) {
            console.error("Error creating post: ", error);
            showFlashMessage("UnknownError, please try again in a few moments", "danger");
            // Reset button state
            submitButton.text(originalButtonText).prop('disabled', false);
        }
    });
}
