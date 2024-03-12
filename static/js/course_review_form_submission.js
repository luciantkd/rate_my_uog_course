document.addEventListener('DOMContentLoaded', function () {
    const feedbackForm = document.getElementById('review');
    feedbackForm.addEventListener('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission
        const formData = new FormData(feedbackForm);
        fetch(feedbackForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message); // Show the alert dialog with the response message
                feedbackForm.reset(); // Reset the form fields to their initial values
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });
});