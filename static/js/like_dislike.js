document.addEventListener('DOMContentLoaded', function() {
    // Get all like buttons
    var likeButtons = document.querySelectorAll('.like-dislike-button');

    // Attach click event listeners to each like button
    likeButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var feedbackId = button.getAttribute('data-feedback-id');
            var likeCount = button.querySelector('.like-count');
            var csrfToken = button.getAttribute('data-csrf-token');
            const url = this.getAttribute('data-url');

            // Send an asynchronous POST request to update the like count
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    feedback_id: feedbackId
                })
            })
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                // Update the like count displayed on the button
                likeCount.textContent = data.likes;

                // Reload the page after successful update
                location.reload();
            })
            .catch(function(error) {
                console.error('Error:', error);
            });
        });
    });
});
