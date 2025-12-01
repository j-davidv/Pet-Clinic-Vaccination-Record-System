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

### Entity Relationship Diagram (ERD)

The system uses a **one-to-many** relationship:
- One Pet can have **many** Vaccination records
- Each Vaccination belongs to **one** Pet

#### Pet Table (Parent)
- `pet_id` (PK)
- `name`, `species`, `breed`
- `date_of_birth`, `gender`, `color`
- `owner_name`, `owner_phone`, `owner_email`, `owner_address`
- `microchip_number` (UNIQUE)
- `registration_date`, `notes`, `is_active`

#### Vaccination Table (Child)
- `vaccination_id` (PK)
- `pet_id` (FK) → References Pet(pet_id)
- `vaccine_name`, `vaccination_date`, `next_due_date`
- `veterinarian_name`, `batch_number`, `manufacturer`
- `dose_number`, `site_administered`
- `adverse_reactions`, `notes`

See `ERD.md` for detailed diagram.

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
├── main.py                      # Main application entry point
├── models.py                    # Pet and Vaccination model classes
├── database.py                  # Database manager with CRUD operations
├── database_schema.sql          # SQL schema for database tables
├── report_generator.py          # PDF report generation
├── gui_add_pet.py              # Add Pet window
├── gui_update_pet.py           # Update Pet window
├── gui_vaccination_records.py  # Vaccination management window
├── gui_reports.py              # Reports generation window
├── requirements.txt            # Python dependencies
├── ERD.md                      # Database ERD documentation
├── README.md                   # This file
├── pet_clinic.db               # SQLite database (created on first run)
└── reports/                    # Generated PDF reports folder
```

## 💡 Usage Guide

### Adding a New Pet

1. Click **"➕ Add Pet"** from the sidebar or dashboard
2. Fill in required fields (marked with *)
3. Enter pet details (name, species, breed, etc.)
4. Enter owner information (name, phone, email, address)
5. Click **"Save Pet"**

### Updating Pet Information

1. Click **"✏️ Update Pet"** from the sidebar
2. Search for the pet or select from the list
3. Click **"Select"** on the desired pet
4. Modify the information as needed
5. Click **"Update Pet"** to save changes

### Managing Vaccinations

1. Click **"💉 Vaccinations"** from the sidebar
2. Select a pet from the dropdown menu
3. Click **"➕ Add Vaccination"** to add a new record
4. Fill in vaccination details (vaccine name, date, etc.)
5. Click **"Save Vaccination"**
6. View, edit, or delete existing vaccination records

### Generating Reports

1. Click **"📄 Reports"** from the sidebar
2. Choose report type:
   - **Individual Pet Report**: Detailed pet and vaccination history
   - **All Pets Report**: Summary of all registered pets
   - **Vaccination Schedule**: Upcoming vaccinations (30 days)
3. Click **"Generate Report"**
4. Report will be saved in the `reports/` folder and opened automatically

### Dashboard Features

- **Statistics Cards**: View total pets, vaccinations, and upcoming appointments
- **Recent Pets**: Quick access to recently registered pets
- **Quick Actions**: Fast navigation to common tasks
- **Appearance Mode**: Switch between Light/Dark/System themes

## 🔧 OOP Principles Implementation

### Encapsulation
- Private attributes with getter/setter properties in model classes
- Data validation within setter methods
- Database operations encapsulated in DatabaseManager class

### Abstraction
- Model classes (Pet, Vaccination) abstract data representation
- Database layer abstracts SQL operations
- Report generator abstracts PDF creation

### Inheritance
- GUI windows inherit from `ctk.CTkToplevel`
- Main app inherits from `ctk.CTk`

### Modularity
- Separate modules for models, database, GUI, and reports
- Single Responsibility Principle applied to each class

## 🗃️ CRUD Operations

### Pet Operations
- **Create**: `db.create_pet(pet)` → Returns pet_id
- **Read**: `db.read_pet(pet_id)` → Returns Pet object
- **Read All**: `db.read_all_pets()` → Returns list of Pet objects
- **Update**: `db.update_pet(pet)` → Returns boolean
- **Delete**: `db.delete_pet(pet_id)` → Returns boolean
- **Search**: `db.search_pets(search_term)` → Returns filtered list

### Vaccination Operations
- **Create**: `db.create_vaccination(vaccination)` → Returns vaccination_id
- **Read**: `db.read_vaccination(vaccination_id)` → Returns Vaccination object
- **Read by Pet**: `db.read_vaccinations_by_pet(pet_id)` → Returns list
- **Update**: `db.update_vaccination(vaccination)` → Returns boolean
- **Delete**: `db.delete_vaccination(vaccination_id)` → Returns boolean

## 📊 Database Features

- **Foreign Key Constraints**: Enforced relationships
- **Cascade Delete**: Deleting a pet removes all its vaccinations
- **Indexes**: Optimized queries on frequently searched fields
- **Soft Delete**: Option to deactivate pets instead of deletion
- **Unique Constraints**: Microchip numbers must be unique

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

## 🔄 Future Enhancements

- Multi-user support with authentication
- Email notifications for upcoming vaccinations
- Backup and restore functionality
- Export data to CSV/Excel
- Appointment scheduling
- Medical history tracking
- Image upload for pets
- Barcode/QR code generation for pets

## 📝 License

This project is created for educational purposes and clinic management use.

---

**Developed with ❤️ using Python and CustomTkinter**