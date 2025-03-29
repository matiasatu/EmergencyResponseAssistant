--delete db file on schema change
CREATE TABLE IF NOT EXISTS user (
    username TEXT PRIMARY KEY,
    phone_number INT NOT NULL,
    email TEXT,
    location TEXT NOT NULL,
    bio TEXT
);

CREATE TABLE IF NOT EXISTS summary (
    username TEXT,
    summary TEXT,
    FOREIGN KEY username REFERNCES user(username)
);