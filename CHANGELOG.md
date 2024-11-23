# Change Log

## [v1.1.2] - 2024-11-23

### Added

- Display today's signups on the homepage.
- Enforced a minimum of two workers per date during signup.
- Duplicate signup detection (same name and date).
- Basic CSS styling for better UI/UX.

### [1.0.1] Date: 2024-11-23


#### Added SQLite Database Integration

Implemented SQLite database to store form entries instead of using an Excel file.
Created a helper function get_db_connection() to connect to the SQLite database.

#### Updated app.py

Added routes to handle form submissions and view entries.
Implemented error handling for missing form fields.
Updated the signup route to store form data in the SQLite database.
Added a new route add_debit to handle debit form submissions and store data in the SQLite database.
Added a new route view_debits to display debit entries.
Updated HTML Templates:

#### signup.html

Ensured form field names match the keys accessed in the Flask route.
Updated form action URL and method.
debit_entry.html:
Ensured form field names match the keys accessed in the Flask route.
Added form fields for name, date, and amount spent.
Added a link to view debit entries.

#### Database Schema

Created a new SQLite database db.sqlite.
Created tables Signups and Debits with appropriate columns.
File Structure:
ExpenaPP/
│
├── app.py
├── db.sqlite
├── templates/
│   ├── home.html
│   ├── signup.html
│   ├── debit_entry.html
│   └── view_debits.html
└── static/
    └── css/
        └── styles.css
Summary:

The application now uses an SQLite database to store form entries.
The signup and debit_entry forms are correctly processed and stored in the database.
Added routes to view signups and debits.
Ensured form field names match the keys accessed in the Flask routes.
Implemented error handling for missing form fields.

## [v1.0.0] - Initial Release

- Basic functionality for volunteer signups and attendance confirmation.
- Credit and debit tracking for volunteers.