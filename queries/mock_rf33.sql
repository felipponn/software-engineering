-- Inserting Users
INSERT INTO Users (name, email, phone_number, role, created_at)
VALUES 
('Alice Smith', 'alice@example.com', '1234567890', 'customer', '2024-10-10 10:00:00'),
('Bob Johnson', 'bob@example.com', '0987654321', 'customer', '2024-10-11 12:00:00'),
('Charlie Brown', 'charlie@example.com', '1122334455', 'admin', '2024-10-12 14:00:00');

-- Inserting Coffee Machines
INSERT INTO Coffee_Machines (location, status, last_serviced_at, installed_at)
VALUES 
('Building A - Lobby', 'operational', '2024-09-15', '2023-12-01'),
('Building B - 2nd Floor', 'under maintenance', '2024-09-10', '2024-01-20'),
('Building C - Cafeteria', 'operational', '2024-09-20', '2024-02-15');

-- Inserting Issues
INSERT INTO Issues (issue_type, description, created_at, resolved_at, status)
VALUES 
('Broken Machine', 'The coffee machine is not dispensing coffee.', '2024-10-12 10:15:00', NULL, 'reported'),
('Out of Coffee', 'The machine is out of coffee beans.', '2024-10-12 11:00:00', NULL, 'reported'),
('App Bug', 'The app crashes when trying to submit a report.', '2024-10-11 14:30:00', NULL, 'in progress'),
('Other', 'The machine dispenses too little coffee.', '2024-10-10 16:45:00', NULL, 'reported');

-- Inserting User Reports
INSERT INTO User_Reports (user_id, machine_id, issue_id, report_description, created_at)
VALUES 
-- Machine-related reports
((SELECT user_id FROM Users WHERE email = 'alice@example.com'), (SELECT machine_id FROM Coffee_Machines WHERE location = 'Building A - Lobby'), 
 (SELECT issue_id FROM Issues WHERE issue_type = 'Broken Machine'), 'Machine stopped working this morning.', '2024-10-12 10:20:00'),
((SELECT user_id FROM Users WHERE email = 'bob@example.com'), (SELECT machine_id FROM Coffee_Machines WHERE location = 'Building B - 2nd Floor'), 
 (SELECT issue_id FROM Issues WHERE issue_type = 'Out of Coffee'), 'Ran out of coffee mid-morning.', '2024-10-12 11:05:00'),

-- General reports not related to a machine
((SELECT user_id FROM Users WHERE email = 'charlie@example.com'), NULL, 
 (SELECT issue_id FROM Issues WHERE issue_type = 'App Bug'), 'The app crashed when submitting a report.', '2024-10-11 14:35:00'),
((SELECT user_id FROM Users WHERE email = 'alice@example.com'), NULL, 
 (SELECT issue_id FROM Issues WHERE issue_type = 'Other'), 'The coffee size is too small, even on large setting.', '2024-10-10 16:50:00');