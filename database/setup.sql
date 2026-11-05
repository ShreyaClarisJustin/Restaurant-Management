CREATE DATABASE IF NOT EXISTS restaurant_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE restaurant_db;

CREATE TABLE IF NOT EXISTS users (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(254) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_email (email)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS foods (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(120) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS orders (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    customer_name VARCHAR(120) NOT NULL,
    quantity INT UNSIGNED NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(40) NOT NULL,
    food_id INT UNSIGNED NOT NULL,
    user_id INT UNSIGNED NOT NULL,
    order_status VARCHAR(40) NOT NULL DEFAULT 'Received',
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY ix_orders_food_id (food_id),
    KEY ix_orders_user_date (user_id, order_date),
    CONSTRAINT fk_orders_food
        FOREIGN KEY (food_id) REFERENCES foods (id),
    CONSTRAINT fk_orders_user
        FOREIGN KEY (user_id) REFERENCES users (id)
) ENGINE=InnoDB;

INSERT IGNORE INTO foods (id, name, price, image_path) VALUES
    (1, 'Chicken Biryani', 220.00, 'images/biryani.jpg'),
    (2, 'Masala Dosa', 120.00, 'images/dosa.jpg'),
    (3, 'Veg Noodles', 160.00, 'images/noodles.jpg');
