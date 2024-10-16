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
