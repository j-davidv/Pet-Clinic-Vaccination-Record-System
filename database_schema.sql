-- Pet Clinic Vaccination Record System Database Schema
-- 3NF: Owner, Pet, VaccineType, and Vaccination tables

-- Owner Table (Parent)
CREATE TABLE IF NOT EXISTS Owner (
    owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    address TEXT,
    UNIQUE(name, phone)
);

-- Pet Table (Child of Owner)
CREATE TABLE IF NOT EXISTS Pet (
    pet_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    species TEXT NOT NULL,
    breed TEXT,
    date_of_birth DATE,
    gender TEXT,
    color TEXT,
    owner_id INTEGER NOT NULL,
    microchip_number TEXT UNIQUE,
    registration_date DATE DEFAULT CURRENT_DATE,
    notes TEXT,
    is_active INTEGER DEFAULT 1,
    FOREIGN KEY (owner_id) REFERENCES Owner(owner_id) ON DELETE CASCADE
);

-- VaccineType Table (Reference data)
CREATE TABLE IF NOT EXISTS VaccineType (
    vaccine_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vaccine_name TEXT NOT NULL UNIQUE,
    manufacturer TEXT
);

-- Vaccination Table (Child of Pet and VaccineType)
CREATE TABLE IF NOT EXISTS Vaccination (
    vaccination_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_id INTEGER NOT NULL,
    vaccine_id INTEGER NOT NULL,
    vaccination_date DATE NOT NULL,
    next_due_date DATE,
    veterinarian_name TEXT,
    batch_number TEXT,
    dose_number INTEGER,
    site_administered TEXT,
    adverse_reactions TEXT,
    notes TEXT,
    FOREIGN KEY (pet_id) REFERENCES Pet(pet_id) ON DELETE CASCADE,
    FOREIGN KEY (vaccine_id) REFERENCES VaccineType(vaccine_id) ON DELETE RESTRICT
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_pet_owner ON Pet(owner_id);
CREATE INDEX IF NOT EXISTS idx_owner_name ON Owner(name);
CREATE INDEX IF NOT EXISTS idx_vaccination_pet ON Vaccination(pet_id);
CREATE INDEX IF NOT EXISTS idx_vaccination_date ON Vaccination(vaccination_date);
CREATE INDEX IF NOT EXISTS idx_next_due_date ON Vaccination(next_due_date);
CREATE INDEX IF NOT EXISTS idx_vaccine_type ON Vaccination(vaccine_id);
