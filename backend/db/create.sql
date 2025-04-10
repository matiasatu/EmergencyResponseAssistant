--delete db file on schema change
CREATE TABLE IF NOT EXISTS user (
    username TEXT PRIMARY KEY,
    phone_number INT NOT NULL,
    email TEXT,
    location TEXT NOT NULL,
    bio TEXT
);

CREATE TABLE IF NOT EXISTS summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    summary TEXT,
    FOREIGN KEY (username) REFERENCES user(username)
);

CREATE TABLE IF NOT EXISTS messages (
    username TEXT,
    output TEXT NOT NULL,
    input TEXT NOT NULL
);