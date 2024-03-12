document.addEventListener('DOMContentLoaded', function () {
    var difficultyProgressBar = document.querySelector('.difficulty-progress-bar');
    var usefulnessProgressBar = document.querySelector('.usefulness-progress-bar');
    var workloadProgressBar = document.querySelector('.workload-progress-bar');
    var professorProgressBar = document.querySelector('.professor-progress-bar');

    // Retrieve the values from data attributes
    var difficultyAvg = parseFloat(difficultyProgressBar.getAttribute('data-value'));
    var usefulnessAvg = parseFloat(usefulnessProgressBar.getAttribute('data-value'));
    var workloadAvg = parseFloat(workloadProgressBar.getAttribute('data-value'));
    var professorAvg = parseFloat(professorProgressBar.getAttribute('data-value'));

    // Convert averages to percentage of the progress bar
    var difficultyWidth = (difficultyAvg / 5) * 100;
    var usefulnessWidth = (usefulnessAvg / 5) * 100;
    var workloadWidth = (workloadAvg / 5) * 100;
    var professorWidth = (professorAvg / 5) * 100;

    // Set the width of the progress bars
    difficultyProgressBar.style.width = difficultyWidth + '%';
    usefulnessProgressBar.style.width = usefulnessWidth + '%';
    workloadProgressBar.style.width = workloadWidth + '%';
    professorProgressBar.style.width = professorWidth + '%';
});
