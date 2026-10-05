
-- 1. Create Customers Table
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    city_tier INT NOT NULL,
    signup_date DATE NOT NULL,
    acquisition_source VARCHAR(20) NOT NULL
);

-- 2. Create Products Table
CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(30) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

-- 3. Create Orders Table
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(10) PRIMARY KEY,
    customer_id VARCHAR(10) NOT NULL,
    product_id VARCHAR(10) NOT NULL,
    order_date DATE NOT NULL,
    quantity INT NOT NULL,
    discount INT,
    payment_method VARCHAR(10) NOT NULL,
    rating INT,
    returned INT NOT NULL DEFAULT 0,

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);