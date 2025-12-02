# Entity Relationship Diagram (ERD)

## Pet Clinic Vaccination Record System (3NF Normalized)

```
┌─────────────────────────────────────┐
│          Owner (Parent)             │
├─────────────────────────────────────┤
│ PK  owner_id (INTEGER)              │
│     name (TEXT) NOT NULL            │
│     phone (TEXT) NOT NULL           │
│     email (TEXT)                    │
│     address (TEXT)                  │
├─────────────────────────────────────┤
│ UNIQUE(name, phone)                 │
│ INDEX(name)                         │
└─────────────────────────────────────┘
                 │
                 │ 1
                 │
                 │
                 │ *
                 ▼
┌─────────────────────────────────────┐
│           Pet (Child)               │
├─────────────────────────────────────┤
│ PK  pet_id (INTEGER)                │
│ FK  owner_id (INTEGER)              │
│     name (TEXT) NOT NULL            │
│     species (TEXT) NOT NULL         │
│     breed (TEXT)                    │
│     date_of_birth (DATE)            │
│     gender (TEXT)                   │
│     color (TEXT)                    │
│     microchip_number (TEXT) UNIQUE  │
│     registration_date (DATE)        │
│     notes (TEXT)                    │
│     is_active (INTEGER)             │
├─────────────────────────────────────┤
│ FK→ Owner(owner_id) CASCADE         │
│ INDEX(owner_id, name)               │
│ INDEX(microchip_number)             │
└─────────────────────────────────────┘
                 │
                 │ 1
                 │
                 │
                 │ *
                 ▼
┌──────────────────────────────────────┐
│      Vaccination (Child)             │
├──────────────────────────────────────┤
│ PK  vaccination_id (INTEGER)         │
│ FK  pet_id (INTEGER)                 │
│ FK  vaccine_id (INTEGER)             │
│     vaccination_date (DATE) NOT NULL │
│     next_due_date (DATE)             │
│     veterinarian_name (TEXT)         │
│     batch_number (TEXT)              │
│     dose_number (INTEGER)            │
│     site_administered (TEXT)         │
│     adverse_reactions (TEXT)         │
│     notes (TEXT)                     │
├──────────────────────────────────────┤
│ FK→ Pet(pet_id) CASCADE              │
│ FK→ VaccineType(vaccine_id)          │
│ INDEX(pet_id, vaccination_date)      │
│ INDEX(next_due_date)                 │
└──────────────────────────────────────┘
           ▲
           │
           │ *
           │
           │ 1
           │
┌──────────────────────────────────────┐
│       VaccineType (Parent)           │
├──────────────────────────────────────┤
│ PK  vaccine_id (INTEGER)             │
│     vaccine_name (TEXT) UNIQUE       │
│     manufacturer (TEXT)              │
├──────────────────────────────────────┤
│ INDEX(vaccine_name)                  │
└──────────────────────────────────────┘
```

## Relationships and Cardinality

### Owner → Pet (1:M)
- **Cardinality**: One Owner has zero or many Pets
- **Foreign Key**: `Pet.owner_id` references `Owner.owner_id`
- **Constraint**: ON DELETE CASCADE (deleting owner removes all their pets)
- **Purpose**: Normalize owner information to avoid duplication

### Pet → Vaccination (1:M)
- **Cardinality**: One Pet has zero or many Vaccination records
- **Foreign Key**: `Vaccination.pet_id` references `Pet.pet_id`
- **Constraint**: ON DELETE CASCADE (deleting pet removes all vaccinations)
- **Purpose**: Track all vaccinations for each pet

### VaccineType → Vaccination (1:M)
- **Cardinality**: One VaccineType has zero or many Vaccinations
- **Foreign Key**: `Vaccination.vaccine_id` references `VaccineType.vaccine_id`
- **Constraint**: ON DELETE RESTRICT (cannot delete vaccine in use)
- **Purpose**: Normalize vaccine information to avoid duplication

## Normalization Principles (3NF)

### First Normal Form (1NF)
✅ All attributes contain atomic (indivisible) values
✅ No repeating groups
✅ Each row is unique

### Second Normal Form (2NF)
✅ Satisfies 1NF
✅ All non-key attributes depend entirely on the primary key
✅ No partial dependencies on composite keys

### Third Normal Form (3NF)
✅ Satisfies 2NF
✅ No transitive dependencies (non-key attributes don't depend on other non-key attributes)
✅ **Owner table eliminates owner data duplication** from Pet table
✅ **VaccineType table eliminates vaccine data duplication** from Vaccination table

## Data Integrity Features

### Primary Keys (PK)
- `Owner.owner_id`: Auto-incrementing integer
- `Pet.pet_id`: Auto-incrementing integer
- `VaccineType.vaccine_id`: Auto-incrementing integer
- `Vaccination.vaccination_id`: Auto-incrementing integer

### Foreign Keys (FK)
- `Pet.owner_id` → `Owner.owner_id` (ON DELETE CASCADE)
- `Vaccination.pet_id` → `Pet.pet_id` (ON DELETE CASCADE)
- `Vaccination.vaccine_id` → `VaccineType.vaccine_id` (ON DELETE RESTRICT)

### Unique Constraints
- `Owner(name, phone)`: Prevents duplicate owner entries
- `Pet.microchip_number`: Ensures unique identification
- `VaccineType.vaccine_name`: Prevents duplicate vaccine types

### Indexes
- `Owner(name)`: Search owners by name
- `Pet(owner_id, name)`: Search pets by owner or name
- `Pet(microchip_number)`: Quick microchip lookup
- `Vaccination(pet_id, vaccination_date)`: Sort vaccinations by date
- `Vaccination(next_due_date)`: Find upcoming vaccinations
- `VaccineType(vaccine_name)`: Search vaccine types by name

### NOT NULL Constraints
- `Owner.name`, `Owner.phone`
- `Pet.name`, `Pet.species`, `Pet.owner_id`
- `VaccineType.vaccine_name`
- `Vaccination.vaccination_date`, `Vaccination.pet_id`, `Vaccination.vaccine_id`

