-- Pet Clinic Vaccination Record System Database Schema
-- ERD: One-to-Many relationship between Pet and Vaccination

-- Pet Table (Parent)
CREATE TABLE IF NOT EXISTS Pet (
    pet_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    species TEXT NOT NULL,
    breed TEXT,
    date_of_birth DATE,
    gender TEXT,
    color TEXT,
    owner_name TEXT NOT NULL,
    owner_phone TEXT NOT NULL,
    owner_email TEXT,
    owner_address TEXT,
    microchip_number TEXT UNIQUE,
    registration_date DATE DEFAULT CURRENT_DATE,
    notes TEXT,
    is_active INTEGER DEFAULT 1
);

-- Vaccination Table (Child)
CREATE TABLE IF NOT EXISTS Vaccination (
    vaccination_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_id INTEGER NOT NULL,
    vaccine_name TEXT NOT NULL,
    vaccination_date DATE NOT NULL,
    next_due_date DATE,
    veterinarian_name TEXT,
    batch_number TEXT,
    manufacturer TEXT,
    dose_number INTEGER,
    site_administered TEXT,
    adverse_reactions TEXT,
    notes TEXT,
    FOREIGN KEY (pet_id) REFERENCES Pet(pet_id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_pet_owner ON Pet(owner_name);
CREATE INDEX IF NOT EXISTS idx_vaccination_pet ON Vaccination(pet_id);
CREATE INDEX IF NOT EXISTS idx_vaccination_date ON Vaccination(vaccination_date);
CREATE INDEX IF NOT EXISTS idx_next_due_date ON Vaccination(next_due_date);
