document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('recommendationForm');
    const recommendationsDiv = document.getElementById('recommendations');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        // Get the SKU ID and state from the form inputs
        const sku_id = document.getElementById('sku_id').value.trim();
        const state = document.getElementById('state').value;

        // Construct the API URL with query parameters
        const apiUrl = `/recommend?sku_id=${sku_id}&state=${state}`;

        // Fetch recommendations from the Flask backend
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                // Clear previous recommendations
                recommendationsDiv.innerHTML = '';

                if (data.error) {
                    recommendationsDiv.innerHTML = `<p>${data.error}</p>`;
                } else if (data.length === 0) {
                    recommendationsDiv.innerHTML = `<p>No recommendations found for the provided SKU ID.</p>`;
                } else {
                    // Display the recommendations
                    data.forEach(item => {
                        const recommendationElement = document.createElement('div');
                        recommendationElement.classList.add('recommendation-item');
                        
                        recommendationElement.innerHTML = `
                            <h3>Product SKU: ${item.sku_id}</h3>
                            <p>Ordered Quantity: ${item.ordered_quantity}</p>
                            <p>Gross Merchandise Value: $${item.gross_merchandise_value.toFixed(2)}</p>
                        `;
                        
                        recommendationsDiv.appendChild(recommendationElement);
                    });
                }
            })
            .catch(error => {
                console.error('Error fetching recommendations:', error);
                recommendationsDiv.innerHTML = '<p>Error fetching recommendations. Please try again later.</p>';
            });
    });
});