-- Users Table
CREATE TABLE Users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(15),
    role VARCHAR(50) DEFAULT 'customer', -- Can be 'customer', 'admin', etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -- Coffee_Machines Table
-- CREATE TABLE Coffee_Machines (
--     machine_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
--     location VARCHAR(255) NOT NULL,
--     status VARCHAR(50) DEFAULT 'operational', -- Status could be 'operational', 'under maintenance', etc.
--     last_serviced_at DATE,
--     installed_at DATE
-- );

-- -- Issues Table
-- CREATE TABLE Issues (
--     issue_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
--     issue_type VARCHAR(255) NOT NULL, -- Type of issue (e.g., "broken", "app issue", "other")
--     description TEXT,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     resolved_at TIMESTAMP, -- Nullable, will be NULL until resolved
--     status VARCHAR(50) DEFAULT 'reported' -- Status could be 'reported', 'in progress', 'resolved', etc.
-- );

-- -- User_Reports Table
-- CREATE TABLE User_Reports (
--     report_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
--     user_id UUID NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE, -- Foreign key to Users
--     machine_id UUID REFERENCES Coffee_Machines(machine_id) ON DELETE SET NULL, -- Nullable, foreign key to Coffee_Machines
--     issue_id UUID NOT NULL REFERENCES Issues(issue_id) ON DELETE CASCADE, -- Foreign key to Issues
--     report_description TEXT,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- -- Indexes and Constraints (Optional but recommended)
-- CREATE INDEX idx_user_reports_user_id ON User_Reports(user_id);
-- CREATE INDEX idx_user_reports_machine_id ON User_Reports(machine_id);
-- CREATE INDEX idx_user_reports_issue_id ON User_Reports(issue_id);