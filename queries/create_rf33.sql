-- Users Table
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,  -- Automatically generates a sequential integer ID
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(15),
    password VARCHAR(255),
    role VARCHAR(50) DEFAULT 'customer',  -- Can be 'customer', 'admin', etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Coffee_Machines Table
CREATE TABLE Coffee_Machines (
    machine_id SERIAL PRIMARY KEY,  -- Automatically generates a sequential integer ID
    location VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'operational',  -- Status could be 'operational', 'under maintenance', etc.
    last_serviced_at DATE,
    installed_at DATE
);

CREATE TABLE User_Reports (
    report_id SERIAL PRIMARY KEY,  -- Automatically generates a sequential integer ID
    user_id INT NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,  -- Foreign key to Users
    machine_id INT REFERENCES Coffee_Machines(machine_id) ON DELETE SET NULL,  -- Nullable, foreign key to Coffee_Machines
    report_target VARCHAR(50) NOT NULL,  -- Target could be 'App' or 'Machine'
    issue_type VARCHAR(255) NOT NULL,  -- The type of issue (e.g., "broken machine", "out of coffee", "app bug", etc.)
    description TEXT,  -- Description of the issue or report
    status VARCHAR(50) DEFAULT 'reported',  -- Status could be 'reported', 'in progress', 'resolved', etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- When the report was created
    resolved_at TIMESTAMP  -- Nullable, to record when the issue was resolved
);

-- Products Table
CREATE TABLE Products (
    product_id SERIAL PRIMARY KEY,  -- Unique ID for each product
    name VARCHAR(255) NOT NULL,  -- Product name
    description TEXT,  -- Description of the product
    price DECIMAL(10, 2) NOT NULL,  -- Price of the product
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Coffee_Machine_Products Table (Many-to-Many relationship)
CREATE TABLE Coffee_Machine_Products (
    machine_id INT NOT NULL REFERENCES Coffee_Machines(machine_id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES Products(product_id) ON DELETE CASCADE,
    quantity INT DEFAULT 0,
    PRIMARY KEY (machine_id, product_id)
);

-- Reviews Table
CREATE TABLE Reviews (
    review_id SERIAL PRIMARY KEY,  -- Unique ID for each review
    user_id INT NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,  -- Reference to the user who wrote the review
    machine_id INT NOT NULL REFERENCES Coffee_Machines(machine_id) ON DELETE CASCADE,  -- Reference to the machine being reviewed
    rating INT CHECK (rating BETWEEN 1 AND 5) NOT NULL,  -- Rating between 1 and 5
    comment TEXT,  -- Optional text comment for the review
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- When the review was created
);

CREATE TABLE User_Selected_Machines (
    user_id INT NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,  -- Reference to the user who selected the machine
    machine_id INT NOT NULL REFERENCES Coffee_Machines(machine_id) ON DELETE CASCADE,  -- Reference to the selected machine
    selected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp of when the machine was selected
    PRIMARY KEY (user_id, machine_id)
);

-- Trigger to check and notify users when a selected machine is out of stock
CREATE OR REPLACE FUNCTION check_out_of_stock() RETURNS TRIGGER AS $$
BEGIN
    -- Check if the selected machine is out of stock
    IF EXISTS (
        SELECT 1
        FROM Coffee_Machine_Products
        WHERE machine_id = NEW.machine_id
        AND quantity = 0
    ) THEN
        -- Insert a notification for the user
        INSERT INTO Notifications (user_id, message, created_at)
        VALUES (
            NEW.user_id,
            'Selected machine is out of stock. Please choose another machine.',
            CURRENT_TIMESTAMP
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER out_of_stock_trigger
AFTER INSERT ON User_Selected_Machines
FOR EACH ROW EXECUTE FUNCTION check_out_of_stock();

-- Notifications Table
CREATE TABLE Notifications (
    notification_id SERIAL PRIMARY KEY,  -- Unique ID for each notification
    user_id INT NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,  -- Reference to the user receiving the notification
    machine_id INT REFERENCES Coffee_Machines(machine_id) ON DELETE SET NULL,  -- Nullable, reference to the machine related to the notification
    product_id INT REFERENCES Products(product_id) ON DELETE SET NULL,  -- Nullable, reference to the product related to the notification
    message TEXT NOT NULL,  -- Notification message
    status VARCHAR(50) DEFAULT 'pending',  -- Status could be 'pending', 'read', 'resolved', etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- When the notification was created
);