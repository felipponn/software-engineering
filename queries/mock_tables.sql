-- Inserting Mock Users
INSERT INTO Users (name, email, phone_number, password, role)
VALUES 
    ('Alice Smith', 'alice@example.com', '1234567890', 'hashed_password1', 'customer'),
    ('Bob Johnson', 'bob@example.com', '0987654321', 'hashed_password2', 'customer');

-- Inserting Mock Coffee Machines
INSERT INTO Coffee_Machines (location, status, last_serviced_at, installed_at)
VALUES 
    ('Building A - Lobby', 'operational', '2024-09-01', '2023-01-15'),
    ('Building B - Kitchen', 'under maintenance', '2024-10-01', '2022-07-20');

-- Inserting Mock User Reports
INSERT INTO User_Reports (user_id, machine_id, report_target, issue_type, description, status, created_at)
VALUES
    ((SELECT user_id FROM Users WHERE email = 'alice@example.com'), 
     (SELECT machine_id FROM Coffee_Machines WHERE location = 'Building A - Lobby'),
     'Machine', 'Broken Machine', 'The coffee machine is not dispensing coffee.', 'resolved', '2024-10-12 10:20:00'),

    ((SELECT user_id FROM Users WHERE email = 'bob@example.com'), 
     NULL, -- No machine_id since it's an app report
     'App', 'App Bug', 'The app crashes when submitting a report.', 'resolved', '2024-10-11 14:35:00');

-- Inserting Mock Products
INSERT INTO Products (name, description, price)
VALUES
    ('Espresso', 'Strong coffee made by forcing steam through ground coffee beans.', 2.50),
    ('Cappuccino', 'Coffee with steamed milk foam.', 3.00),
    ('Latte', 'Coffee with steamed milk.', 3.50);

-- Inserting Mock Coffee Machine Products (with quantities)
INSERT INTO Coffee_Machine_Products (machine_id, product_id, quantity)
VALUES
    ((SELECT machine_id FROM Coffee_Machines WHERE location = 'Building A - Lobby'),
     (SELECT product_id FROM Products WHERE name = 'Espresso'), 10),

    ((SELECT machine_id FROM Coffee_Machines WHERE location = 'Building A - Lobby'),
     (SELECT product_id FROM Products WHERE name = 'Cappuccino'), 5),

    ((SELECT machine_id FROM Coffee_Machines WHERE location = 'Building B - Kitchen'),
     (SELECT product_id FROM Products WHERE name = 'Latte'), 0);  -- Out of stock

-- Inserting Mock Reviews
INSERT INTO Reviews (user_id, machine_id, rating, comment, created_at)
VALUES
    ((SELECT user_id FROM Users WHERE email = 'alice@example.com'), 
     (SELECT machine_id FROM Coffee_Machines WHERE location = 'Building A - Lobby'), 
     5, 'Great coffee, fast service!', '2024-10-15 09:45:00'),

    ((SELECT user_id FROM Users WHERE email = 'bob@example.com'), 
     (SELECT machine_id FROM Coffee_Machines WHERE location = 'Building B - Kitchen'), 
     3, 'Decent coffee, but machine is often down.', '2024-10-16 13:15:00');

-- Inserting Mock User Selected Machines
INSERT INTO User_Selected_Machines (user_id, machine_id)
VALUES
    ((SELECT user_id FROM Users WHERE email = 'alice@example.com'), 
     (SELECT machine_id FROM Coffee_Machines WHERE location = 'Building A - Lobby')),

    ((SELECT user_id FROM Users WHERE email = 'bob@example.com'), 
     (SELECT machine_id FROM Coffee_Machines WHERE location = 'Building B - Kitchen'));

-- Insert Mock User Product Reviews
INSERT INTO Product_Reviews (user_id, product_id, rating, created_at)
VALUES
    ((SELECT user_id FROM Users WHERE email = 'alice@example.com'), 
     (SELECT product_id FROM Products WHERE name = 'Espresso'), 
     4, 'Great espresso, perfect for mornings!', '2024-10-15 09:45:00'),

    ((SELECT user_id FROM Users WHERE email = 'bob@example.com'), 
     (SELECT product_id FROM Products WHERE name = 'Cappuccino'), 
     3, 'Decent cappuccino, could be creamier.', '2024-10-16 13:15:00'),

    ((SELECT user_id FROM Users WHERE email = 'alice@example.com'), 
     (SELECT product_id FROM Products WHERE name = 'Latte'), 
     5, 'Best latte I''ve ever had!', '2024-10-16 09:45:00');