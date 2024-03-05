function convertToStars(rating) {
    const maxStars = 5;
    const fullStars = Math.floor(rating);
    const halfStar = (rating % 1) >= 0.5 ? 1 : 0;
    let stars = '★'.repeat(fullStars);
    stars += halfStar ? '⭐' : ''; // ⭐ represents a half-star character, or you can use '★' with a different class
    stars += '☆'.repeat(maxStars - fullStars - halfStar);
    return stars;;
  }
  
  // Convert all ratings to stars once the document is loaded
  document.addEventListener('DOMContentLoaded', () => {
    const ratings = document.querySelectorAll('.star-rating');
    ratings.forEach(span => {
      const rating = parseInt(span.getAttribute('data-rating'));
      span.textContent = convertToStars(rating);
    });
  });