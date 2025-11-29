# QUITESCAN Database Tables for ERD Research

## Table 1: Students
**Purpose**: Stores student information and QR code data for attendance tracking

| Field Name | Data Type | Length | Constraints | Description |
|------------|-----------|--------|-------------|-------------|
| id | INT | - | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for each student |
| student_id | VARCHAR | 20 | UNIQUE, NOT NULL | Student identification number |
| first_name | VARCHAR | 50 | NOT NULL | Student's first name |
| last_name | VARCHAR | 50 | NOT NULL | Student's last name |
| email | VARCHAR | 100 | UNIQUE, NOT NULL | Student's email address |
| qr_code | VARCHAR | 255 | UNIQUE, NOT NULL | Generated QR code string |
| qr_image_path | VARCHAR | 255 | NULL | Path to QR code image file |
| created_at | TIMESTAMP | - | DEFAULT CURRENT_TIMESTAMP | Registration timestamp |
| status | ENUM | - | ('active', 'inactive'), DEFAULT 'active' | Student account status |

**Relationships**: 
- One-to-Many with attendance_logs (One student can have many attendance records)

---

## Table 2: Admins
**Purpose**: Manages administrative user accounts for system access control

| Field Name | Data Type | Length | Constraints | Description |
|------------|-----------|--------|-------------|-------------|
| id | INT | - | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for each admin |
| username | VARCHAR | 50 | UNIQUE, NOT NULL | Administrative username |
| password | VARCHAR | 255 | NOT NULL | Encrypted password hash |
| email | VARCHAR | 100 | UNIQUE, NOT NULL | Administrator's email |
| created_at | TIMESTAMP | - | DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |

**Relationships**: 
- No direct foreign key relationships (Independent table for authentication)

---

## Table 3: Attendance_Logs
**Purpose**: Records all student check-in and check-out activities

| Field Name | Data Type | Length | Constraints | Description |
|------------|-----------|--------|-------------|-------------|
| id | INT | - | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for each record |
| student_id | INT | - | FOREIGN KEY, NOT NULL | References students.id |
| action | ENUM | - | ('IN', 'OUT'), NOT NULL | Check-in or check-out action |
| timestamp | TIMESTAMP | - | DEFAULT CURRENT_TIMESTAMP | Date and time of attendance |

**Relationships**: 
- Many-to-One with students (Many attendance records belong to one student)
- Foreign Key: student_id REFERENCES students(id) ON DELETE CASCADE

---

## Entity Relationship Summary

### Primary Relationships:
1. **Students (1) ←→ (Many) Attendance_Logs**
   - Relationship Type: One-to-Many
   - Foreign Key: attendance_logs.student_id → students.id
   - Cascade Rule: ON DELETE CASCADE

### Table Connections for ERD:
```
┌─────────────┐         ┌──────────────────┐
│   Students  │ 1    ∞  │ Attendance_Logs  │
│             │─────────│                  │
│ • id (PK)   │         │ • id (PK)        │
│ • student_id│         │ • student_id (FK)│
│ • first_name│         │ • action         │
│ • last_name │         │ • timestamp      │
│ • email     │         └──────────────────┘
│ • qr_code   │
│ • qr_image  │
│ • created_at│
│ • status    │
└─────────────┘

┌─────────────┐
│   Admins    │ (Independent)
│             │
│ • id (PK)   │
│ • username  │
│ • password  │
│ • email     │
│ • created_at│
└─────────────┘
```

## Database Constraints and Indexes

### Unique Constraints:
- students.student_id (Prevents duplicate student IDs)
- students.email (Prevents duplicate email addresses)
- students.qr_code (Ensures unique QR codes)
- admins.username (Prevents duplicate usernames)
- admins.email (Prevents duplicate admin emails)

### Foreign Key Constraints:
- attendance_logs.student_id → students.id (CASCADE DELETE)

### Indexes (Recommended):
- PRIMARY KEY indexes (automatic)
- INDEX on attendance_logs.timestamp (for date-based queries)
- INDEX on attendance_logs.student_id (for student-specific queries)
- INDEX on students.status (for active/inactive filtering)

## Data Integrity Rules

1. **Referential Integrity**: All attendance records must reference valid students
2. **Domain Integrity**: ENUM fields restrict values to predefined options
3. **Entity Integrity**: All tables have primary keys ensuring unique records
4. **User-Defined Integrity**: Unique constraints prevent duplicate critical data

This database design supports efficient querying, maintains data consistency, and provides a solid foundation for the QUITESCAN attendance management system.