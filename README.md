# Backend Engineer (Intern): Flask E-Commerce API

## Objective

Create a Flask-based backend API for a basic e-commerce platform, demonstrating your understanding of RESTful API development and database integration.

## Requirements

### Setup

- Initialize a new Flask application.
- Set up a database using SQLite or any other database of your choice.
- (Optional) Use Flask-RESTful for creating the API endpoints.

### Models

Create the following models:

- `Product`: Represents a product with fields such as `id`, `name`, `description`, `price`, and `image_url`.
- `CartItem`: Represents an item in a cart with fields such as `id`, `product_id`, and `quantity`.

### API Endpoints

Create the following RESTful API endpoints:

- `GET /products`: Returns a list of all products.
- `GET /products/<id>`: Returns details of a specific product.
- `POST /cart`: Adds a product to the cart.
- `GET /cart`: Retrieves the cart items.
- `DELETE /cart/<id>`: Removes a specific item from the cart.

### Database Integration

- Set up the database and create the necessary tables for your models.
- Implement CRUD operations for interacting with the database.

## Submission

- Submit your code as a ZIP file or provide a link to a GitHub repository containing the project.
- Ensure that your application runs without errors and demonstrates the required functionality.

## Evaluation Criteria

- Code structure and readability.
- Correct implementation of RESTful API endpoints.
- Proper database integration and handling of CRUD operations.
- Overall functionality of the API.
