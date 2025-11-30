-- Simple sample database for PostgreSQL agent
-- This creates a small e-commerce database with sample data

-- Create tables
CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    category VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL
);

-- Insert sample data (idempotent - safe to run multiple times)
INSERT INTO customers (first_name, last_name, email) VALUES
    ('John', 'Doe', 'john.doe@example.com'),
    ('Jane', 'Smith', 'jane.smith@example.com'),
    ('Bob', 'Johnson', 'bob.johnson@example.com'),
    ('Alice', 'Williams', 'alice.williams@example.com'),
    ('Charlie', 'Brown', 'charlie.brown@example.com')
ON CONFLICT (email) DO NOTHING;

-- Insert products (using DO block to check if data exists first)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM products LIMIT 1) THEN
        INSERT INTO products (name, description, price, stock_quantity, category) VALUES
            ('Laptop', 'High-performance laptop', 999.99, 15, 'Electronics'),
            ('Mouse', 'Wireless mouse', 29.99, 50, 'Electronics'),
            ('Keyboard', 'Mechanical keyboard', 79.99, 30, 'Electronics'),
            ('Monitor', '27-inch 4K monitor', 399.99, 20, 'Electronics'),
            ('Desk Chair', 'Ergonomic office chair', 199.99, 10, 'Furniture'),
            ('Desk', 'Standing desk', 299.99, 8, 'Furniture'),
            ('Notebook', 'Premium notebook', 12.99, 100, 'Stationery'),
            ('Pen Set', 'Fountain pen set', 49.99, 25, 'Stationery');
    END IF;
END $$;

-- Only insert orders if they don't exist (check by order_id)
INSERT INTO orders (order_id, customer_id, total_amount, status) VALUES
    (1, 1, 1029.98, 'completed'),
    (2, 2, 479.98, 'completed'),
    (3, 3, 79.99, 'pending'),
    (4, 1, 199.99, 'shipped'),
    (5, 4, 349.98, 'completed')
ON CONFLICT (order_id) DO NOTHING;

-- Only insert order items if they don't exist (check by order_item_id)
INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price) VALUES
    (1, 1, 1, 1, 999.99),
    (2, 1, 2, 1, 29.99),
    (3, 2, 4, 1, 399.99),
    (4, 2, 5, 1, 79.99),
    (5, 3, 3, 1, 79.99),
    (6, 4, 5, 1, 199.99),
    (7, 5, 6, 1, 299.99),
    (8, 5, 2, 1, 29.99),
    (9, 5, 7, 1, 12.99),
    (10, 5, 8, 1, 7.99)
ON CONFLICT (order_item_id) DO NOTHING;

-- Create some useful views
CREATE OR REPLACE VIEW customer_orders AS
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    o.order_id,
    o.order_date,
    o.total_amount,
    o.status
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;

CREATE OR REPLACE VIEW product_sales AS
SELECT 
    p.product_id,
    p.name AS product_name,
    p.category,
    SUM(oi.quantity) AS total_sold,
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name, p.category;

