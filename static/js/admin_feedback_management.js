document.addEventListener('DOMContentLoaded', function () {
    var friendlyProgressBar = document.querySelector('.friendly-progress-bar');
    var aestheticProgressBar = document.querySelector('.aesthetic-progress-bar');

    // Retrieve the values from data attributes
    var friendlyAvg = parseFloat(friendlyProgressBar.getAttribute('data-value'));
    var aestheticAvg = parseFloat(aestheticProgressBar.getAttribute('data-value'));

    // Convert averages to percentage of the progress bar
    var friendlyWidth = (friendlyAvg / 5) * 100;
    var aestheticWidth = (aestheticAvg / 5) * 100;

    // Set the width of the progress bars
    friendlyProgressBar.style.width = friendlyWidth + '%';
    aestheticProgressBar.style.width = aestheticWidth + '%';
});
