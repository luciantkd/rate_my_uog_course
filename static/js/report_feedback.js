document.addEventListener('DOMContentLoaded', function() {
    const reportButtons = document.querySelectorAll('.report-button');
    reportButtons.forEach(button => {
        button.addEventListener('click', function() {
            const feedbackId = this.getAttribute('data-feedback-id');
            const csrfToken = this.getAttribute('data-csrf-token');
            const url = this.getAttribute('data-url'); // Access the URL from the data attribute

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 'feedback_id': feedbackId })
            })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                alert('Report successfully submitted.');
            })
            .catch(error => {
                console.error('Error:', error);
                alert('There was a problem submitting your report.');
            });
        });
    });
});
