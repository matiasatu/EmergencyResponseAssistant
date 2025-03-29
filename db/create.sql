--delete db file on schema change
CREATE TABLE IF NOT EXISTS user (
    username TEXT PRIMARY KEY,
    phone_number INT NOT NULL,
    email TEXT,
    zipcode INT NOT NULL,
    bio TEXT
);