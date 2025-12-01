# Entity Relationship Diagram (ERD)

## Pet Clinic Vaccination Record System

```
┌─────────────────────────────────────┐
│             Pet (Parent)            │
├─────────────────────────────────────┤
│ PK  pet_id (INTEGER)                │
│     name (TEXT)                     │
│     species (TEXT)                  │
│     breed (TEXT)                    │
│     date_of_birth (DATE)            │
│     gender (TEXT)                   │
│     color (TEXT)                    │
│     owner_name (TEXT)               │
│     owner_phone (TEXT)              │
│     owner_email (TEXT)              │
│     owner_address (TEXT)            │
│     microchip_number (TEXT) UNIQUE  │
│     registration_date (DATE)        │
│     notes (TEXT)                    │
│     is_active (INTEGER)             │
└─────────────────────────────────────┘
                 │
                 │ 1
                 │
                 │
                 │ *
                 ▼
┌─────────────────────────────────────┐
│        Vaccination (Child)          │
├─────────────────────────────────────┤
│ PK  vaccination_id (INTEGER)        │
│ FK  pet_id (INTEGER)                │
│     vaccine_name (TEXT)             │
│     vaccination_date (DATE)         │
│     next_due_date (DATE)            │
│     veterinarian_name (TEXT)        │
│     batch_number (TEXT)             │
│     manufacturer (TEXT)             │
│     dose_number (INTEGER)           │
│     site_administered (TEXT)        │
│     adverse_reactions (TEXT)        │
│     notes (TEXT)                    │
└─────────────────────────────────────┘
```

## Relationship Description

**One-to-Many Relationship:**
- One Pet can have **many** Vaccination records
- Each Vaccination record belongs to **one** Pet
- Foreign Key: `Vaccination.pet_id` references `Pet.pet_id`
- Cascade delete: When a Pet is deleted, all associated Vaccinations are deleted

## Business Rules

1. Each pet must have a unique pet_id (Primary Key)
2. Pet name and owner information are mandatory
3. Microchip numbers must be unique if provided
4. Each vaccination must be linked to a valid pet
5. Vaccination dates and vaccine names are mandatory
6. Next due dates help track upcoming vaccinations
