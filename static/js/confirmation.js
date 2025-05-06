document.addEventListener("DOMContentLoaded", function () {
    document
      .querySelector(".btn-primary")
      .addEventListener("click", function () {
        let reviews = [];
  
        document.querySelectorAll(".review-item").forEach((item) => {
          let checkbox = item.querySelector(".form-check-input");
          if (checkbox.checked) {
            let rating = item.querySelector(".rating").value;
            let reviewText = item.querySelector(".review-textarea").value;
            let productId = checkbox.getAttribute("data-product-id");
  
            reviews.push({
              product_id: productId,
              rating: rating,
              review_text: reviewText,
            });
          }
        });
  
        fetch(submitReviewsURL, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ reviews: reviews }),
        })
          .then((response) => response.json())
          .then((data) => {
            alert(data.message);
            window.location.href = "/";
          })
          .catch((error) => {
            console.error("Error:", error);
            alert("Failed to submit reviews");
          });
      });
  });
  