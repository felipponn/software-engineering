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