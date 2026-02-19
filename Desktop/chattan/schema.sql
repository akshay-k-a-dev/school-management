-- SQLite schema for Campus Service Hub (chattan.db)
-- Run this with: sqlite3 chattan.db < schema.sql
-- Note: SQLAlchemy will create tables automatically; this file is provided for reference / manual creation.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'student',
  phone VARCHAR(32) DEFAULT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS complaints (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  title TEXT,
  description TEXT,
  category TEXT,
  status TEXT DEFAULT 'pending',
  assigned_to INTEGER DEFAULT NULL,
  image_path TEXT DEFAULT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  description TEXT,
  date DATETIME,
  venue TEXT,
  capacity INTEGER,
  created_by INTEGER,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS event_registrations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id INTEGER,
  user_id INTEGER,
  registered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (event_id) REFERENCES events(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS bookings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  room_name TEXT,
  date DATE,
  start_time TIME,
  end_time TIME,
  status TEXT DEFAULT 'pending',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS announcements (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  content TEXT,
  created_by INTEGER,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  attachment TEXT DEFAULT NULL,
  FOREIGN KEY (created_by) REFERENCES users(id)
);
