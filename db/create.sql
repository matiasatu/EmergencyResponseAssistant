--delete db file on schema change
CREATE TABLE IF NOT EXISTS user (
    username TEXT PRIMARY KEY,
    phone_number INT,
    email TEXT,
    zipcode INT,
    bio TEXT
);