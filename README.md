# Pet Clinic Vaccination Record System

A comprehensive desktop application for managing pet information and vaccination schedules at veterinary clinics. Built with Python using modern GUI frameworks and following Object-Oriented Programming principles.

## 🌟 Features

### Core Functionality
- **Pet Management**: Complete CRUD operations for pet records
- **Vaccination Tracking**: Schedule and manage vaccination records
- **Owner Information**: Store and manage pet owner contact details
- **Report Generation**: Create professional PDF reports
- **Search & Filter**: Quick search functionality for pets and records
- **Dashboard Analytics**: Real-time statistics and upcoming vaccination alerts

### User Interface
- **Main Dashboard**: Overview with statistics and quick actions
- **Add Pet Window**: Form-based pet registration with validation
- **Update Pet Window**: Edit existing pet information
- **Vaccination Records View**: Manage vaccination history
- **Reports Window**: Generate various PDF reports
- **Modern UI**: Built with CustomTkinter for a clean, modern look

## 🗄️ Database Design

### Database Normalization (3NF)

The system uses a **normalized relational database** following the Third Normal Form (3NF) to eliminate redundancy and ensure data integrity:

- **Owner** table: Separate owner information
- **Pet** table: Pet information with FK to Owner
- **VaccineType** table: Vaccine information (eliminates duplication)
- **Vaccination** table: Vaccination records with FKs to Pet and VaccineType

#### Owner Table
- `owner_id` (PK, Auto-increment)
- `name` (NOT NULL)
- `phone` (NOT NULL)
- `email`
- `address`
- **Unique Constraint**: (name, phone) combination

#### Pet Table (Child of Owner)
- `pet_id` (PK, Auto-increment)
- `name` (NOT NULL)
- `species` (NOT NULL)
- `breed`
- `gender`
- `color`
- `date_of_birth`
- `owner_id` (FK) → References Owner(owner_id) ON DELETE CASCADE
- `microchip_number` (UNIQUE)
- `registration_date`
- `notes`
- `is_active` (Default: 1)

#### VaccineType Table
- `vaccine_id` (PK, Auto-increment)
- `vaccine_name` (UNIQUE, NOT NULL)
- `manufacturer`

#### Vaccination Table (Child of Pet & VaccineType)
- `vaccination_id` (PK, Auto-increment)
- `pet_id` (FK) → References Pet(pet_id) ON DELETE CASCADE
- `vaccine_id` (FK) → References VaccineType(vaccine_id)
- `vaccination_date` (NOT NULL)
- `next_due_date`
- `veterinarian_name`
- `batch_number`
- `dose_number`
- `site_administered`
- `adverse_reactions`
- `notes`

#### Entity Relationships
- One **Owner** → Many **Pets** (1:M)
- One **Pet** → Many **Vaccinations** (1:M)
- One **VaccineType** → Many **Vaccinations** (1:M)

### Benefits of 3NF Design
✅ **Eliminates Redundancy**: Owner data stored once, not repeated per pet  
✅ **Eliminates Vaccine Duplication**: Vaccine names stored once, referenced by ID  
✅ **Data Consistency**: Single source of truth for owner and vaccine information  
✅ **Referential Integrity**: Foreign key constraints prevent orphaned records  
✅ **Cascade Deletes**: Deleting an owner automatically removes their pets and vaccinations  
✅ **Efficient Queries**: Indexed foreign keys for optimal JOIN performance

See `ERD.md` for detailed Entity Relationship Diagram.

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Programming Language | Python 3.8+ |
| GUI Framework | CustomTkinter |
| Database | SQLite3 |
| PDF Reports | ReportLab |
| Date Picker | tkcalendar |
| Table Display | PrettyTable |
| Image Processing | Pillow |

## 📋 Prerequisites

- Python 3.8 or higher
- Windows OS (tested on Windows 10/11)
- pip (Python package manager)

## 🚀 Installation

### 1. Clone or Download the Repository

```powershell
cd e:\USER\Downloads\Pet-Clinic-Vaccination-Record-System
```

### 2. Create Virtual Environment (Recommended)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run the Application

```powershell
python main.py
```

## 📁 Project Structure

```
Pet-Clinic-Vaccination-Record-System/
├── main.py                      # Main application entry point and dashboard
├── models.py                    # Data model classes: Owner, Pet, VaccineType, Vaccination
├── database.py                  # Database manager with CRUD operations for all tables
├── database_schema.sql          # SQL schema for normalized 3NF database
├── report_generator.py          # PDF report generation with ReportLab
├── gui_add_pet.py              # GUI window for adding new pets and owners
├── gui_update_pet.py           # GUI window for updating pets and owner information
├── gui_vaccination_records.py  # GUI window for vaccination management
├── gui_reports.py              # GUI window for report generation
├── debug_test.py               # Comprehensive test suite for all operations
├── requirements.txt            # Python dependencies and versions
├── ERD.md                      # Entity Relationship Diagram documentation
├── README.md                   # This file
├── pet_clinic.db               # SQLite database (created on first run)
├── reports/                    # Generated PDF reports folder
└── __pycache__/                # Python bytecode cache directory
```

### Model Classes (models.py)
- **Owner**: Represents pet owners with contact information
- **Pet**: Represents pets with normalized owner_id foreign key
- **VaccineType**: Represents vaccine types (name, manufacturer)
- **Vaccination**: Represents vaccination records with vaccine_id and pet_id foreign keys

## 💡 Usage Guide

### Adding a New Pet

1. Click **"➕ Add Pet"** from the sidebar or dashboard
2. **Owner Section**: 
   - Enter owner details (name, phone, email, address)
   - The system will check for existing owners with same name and phone
   - A new owner record is created if one doesn't exist
3. **Pet Section**:
   - Enter required pet details: name, species, breed (marked with *)
   - Optional: date of birth, gender, color, microchip number, notes
4. Click **"Save Pet"** to create both owner and pet records

### Updating Pet Information

1. Click **"✏️ Update Pet"** from the sidebar
2. Search for the pet or select from the list
3. Click **"Select"** on the desired pet
4. Update **Owner Information**:
   - Modify owner details (name, phone, email, address)
   - Owner record is updated if pet is linked to existing owner
5. Update **Pet Information**:
   - Modify any pet details as needed
6. Click **"Update Pet"** to save all changes

### Managing Vaccinations

1. Click **"💉 Vaccinations"** from the sidebar
2. Select a pet from the dropdown menu
3. Click **"➕ Add Vaccination"** to add a new record
4. **Vaccine Type**:
   - Select from existing vaccines in the dropdown
   - Or type a new vaccine name (auto-created if doesn't exist)
5. Fill in vaccination details:
   - Vaccination date (required)
   - Next due date (optional, calculated automatically)
   - Veterinarian name, batch number, dose number
   - Site administered, adverse reactions, notes
6. Click **"Save Vaccination"**
7. View, edit, or delete existing vaccination records
8. Each vaccination displays the vaccine name and linked pet information

### Generating Reports

1. Click **"📄 Reports"** from the sidebar
2. Choose report type:
   - **Individual Pet Report**: 
     - Displays complete pet and owner information
     - Shows full vaccination history with vaccine names
     - Includes notes and additional information
   - **All Pets Report**: 
     - Summary table of all active pets with owner names
     - Quick reference guide
   - **Vaccination Schedule**: 
     - Upcoming vaccinations for next 30 days
     - Pet names, owners, and due dates
     - Formatted for clinic scheduling
3. Click **"Generate Report"**
4. Report will be saved in the `reports/` folder as PDF
5. Report automatically opens after generation

### Dashboard Features

- **Statistics Cards**: View total pets, vaccinations, and upcoming appointments
- **Recent Pets**: Quick access to recently registered pets
- **Quick Actions**: Fast navigation to common tasks
- **Appearance Mode**: Switch between Light/Dark/System themes


## 🗃️ CRUD Operations

### Owner Operations
- **Create**: `db.create_owner(owner)` → Returns owner_id
- **Read**: `db.read_owner(owner_id)` → Returns Owner object
- **Read All**: `db.read_all_owners()` → Returns list of Owner objects
- **Update**: `db.update_owner(owner)` → Returns boolean
- **Delete**: `db.delete_owner(owner_id)` → Returns boolean

### Pet Operations
- **Create**: `db.create_pet(pet)` → Returns pet_id
- **Read**: `db.read_pet(pet_id)` → Returns Pet object
- **Read All**: `db.read_all_pets()` → Returns list of Pet objects
- **Update**: `db.update_pet(pet)` → Returns boolean
- **Delete**: `db.delete_pet(pet_id)` → Returns boolean (cascades to vaccinations)
- **Search**: `db.search_pets(search_term)` → Returns filtered list (searches by name and owner)

### VaccineType Operations
- **Create**: `db.create_vaccine_type(vaccine)` → Returns vaccine_id
- **Read**: `db.read_vaccine_type(vaccine_id)` → Returns VaccineType object
- **Read All**: `db.read_all_vaccine_types()` → Returns list of VaccineType objects
- **Update**: `db.update_vaccine_type(vaccine)` → Returns boolean
- **Delete**: `db.delete_vaccine_type(vaccine_id)` → Returns boolean

### Vaccination Operations
- **Create**: `db.create_vaccination(vaccination)` → Returns vaccination_id
- **Read**: `db.read_vaccination(vaccination_id)` → Returns Vaccination object
- **Read by Pet**: `db.read_vaccinations_by_pet(pet_id)` → Returns list of Vaccination objects
- **Read All**: `db.read_all_vaccinations()` → Returns list of all Vaccination objects
- **Update**: `db.update_vaccination(vaccination)` → Returns boolean
- **Delete**: `db.delete_vaccination(vaccination_id)` → Returns boolean

### Utility Operations
- **Upcoming Vaccinations**: `db.get_upcoming_vaccinations(days=30)` → Returns tuples with joined pet and vaccine info
- **Vaccination Count**: `db.get_vaccination_count()` → Returns total count

## 📊 Database Features

### Normalization (Third Normal Form - 3NF)
- **Separate Tables**: Owner and VaccineType extracted as independent entities
- **No Data Duplication**: Owner info stored once per owner, vaccine info stored once per vaccine type
- **Foreign Keys**: Pet references Owner by owner_id, Vaccination references Pet and VaccineType by IDs
- **Referential Integrity**: Database enforces all relationships through constraints

### Data Integrity
- **Foreign Key Constraints**: Enforced relationships between tables
- **Cascade Delete**: Deleting an owner or pet automatically removes related records
- **Unique Constraints**: 
  - Microchip numbers are unique per pet
  - Vaccine names are unique
  - Owner (name, phone) combination is unique
- **NOT NULL Constraints**: Required fields enforced at database level
- **Indexes**: Optimized queries on frequently searched fields (pet_id, owner_id, vaccine_id, vaccination_date)

### Query Performance
- **Indexed Foreign Keys**: Fast lookups and JOINs
- **Indexed Date Fields**: Efficient filtering by vaccination dates
- **Pre-joined Data**: `get_upcoming_vaccinations()` returns already-joined results

### Data Consistency
- **Transaction Support**: Database operations are atomic
- **PRAGMA foreign_keys = ON**: Foreign key constraints always enforced
- **Connection Management**: Singleton pattern ensures single database connection

## 🎨 GUI Components

### Main Dashboard
- Statistics overview
- Recent pets list
- Quick action buttons
- Theme customization

### Form Validation
- Required field checking
- Email format validation
- Phone number validation
- Date validation

### User Experience
- Modal windows for focused tasks
- Scrollable frames for long content
- Responsive layouts
- Error handling with user-friendly messages

## 📄 Report Types

### Individual Pet Report
- Complete pet information
- Owner contact details
- Full vaccination history
- Additional notes

### All Pets Report
- Summary table of all pets
- Owner information
- Quick reference guide

### Vaccination Schedule
- Upcoming vaccinations (30 days)
- Pet and owner contact info
- Due dates highlighted

## 🔒 Data Validation

- **Required Fields**: Name, species, owner name, owner phone
- **Email Format**: Regex validation for email addresses
- **Phone Format**: Minimum length validation
- **Date Validation**: Using tkcalendar for proper date selection
- **Microchip Uniqueness**: Database constraint enforcement

## 🐛 Troubleshooting

### Database Errors
- Ensure `pet_clinic.db` has write permissions
- Check for duplicate microchip numbers

### Import Errors
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Activate virtual environment if using one

### GUI Issues
- Update CustomTkinter: `pip install --upgrade customtkinter`
- Check Python version (3.8+)

### Report Generation Fails
- Ensure `reports/` folder exists (created automatically)
- Check ReportLab installation

### Test Output Example
```
==================================================
Pet Clinic Vaccination System - Debug Test
==================================================

=== Testing Owner Operations ===
✓ Owner created: ID=1, Name=John Doe
✓ Owner read: John Doe, Phone=555-1234
✓ Owner updated: Phone=555-5678
✓ All owners retrieved: 1 total

=== Testing Vaccine Type Operations ===
✓ Vaccine created: ID=1, Name=Rabies
✓ Vaccine read: Rabies, Manufacturer=Zoetis
✓ All vaccines retrieved: 1 total

[... more test results ...]

✓ Pet report generated: pet_report_Buddy_20251202_110306.pdf
✓ All pets report generated: all_pets_report_20251202_110306.pdf
✓ Vaccination schedule report generated: vaccination_schedule_20251202_110306.pdf

==================================================
Debug test completed!
==================================================
```

## 📝 License

This project is created for educational purposes and clinic management use.

---

**Developed with ❤️ using Python and CustomTkinter**