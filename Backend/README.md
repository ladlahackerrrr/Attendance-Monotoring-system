# Student Attendance Registration System

A web-based student attendance management system built with Flask for BCA 5th Semester Minor Project.

## Features

### Admin Features
- Secure authentication
- Manage classes (Add/View/Delete)
- Manage students and assign to classes
- Manage teachers and assign classes
- View all attendance records

### Teacher Features
- Secure login
- View assigned classes
- Mark attendance (Present/Absent)
- View attendance history
- Prevent duplicate entries for same date

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript
- **Database**: SQLite
- **Authentication**: Session-based with password hashing

## Installation & Setup

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd student-attendance-system
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser and go to: `http://localhost:5000`

## Default Login Credentials

### Administrator
- **Email**: admin@school.com
- **Password**: admin123

### Teachers
Teachers need to be created by the administrator through the admin panel.

## Database Structure

The system uses SQLite with the following tables:

- **classes**: Store class information (id, name, section)
- **students**: Store student details (id, name, roll_no, class_id)
- **teachers**: Store teacher credentials (id, name, email, password_hash)
- **teacher_classes**: Link teachers to their assigned classes
- **attendance**: Store attendance records (id, date, class_id, student_id, status)

## Usage Guide

### For Administrators

1. **Login** with admin credentials
2. **Add Classes**: Create classes with name and section
3. **Add Students**: Register students and assign them to classes
4. **Add Teachers**: Create teacher accounts and assign classes
5. **View Records**: Monitor all attendance records

### For Teachers

1. **Login** with teacher credentials
2. **Select Class**: Choose from assigned classes
3. **Take Attendance**: Mark students as Present/Absent
4. **Save**: Submit attendance (prevents duplicates for same date)
5. **View History**: Check previously recorded attendance

## Project Structure

```
student-attendance-system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── attendance.db         # SQLite database (created automatically)
└── templates/            # HTML templates
    ├── base.html
    ├── login.html
    ├── admin_dashboard.html
    ├── admin_attendance_records.html
    ├── teacher_dashboard.html
    ├── take_attendance.html
    └── teacher_attendance_history.html
```

## Key Features Implemented

✅ **Authentication System**: Role-based login (Admin/Teacher)  
✅ **CRUD Operations**: Complete Create, Read, Update, Delete functionality  
✅ **Database Integration**: SQLite with proper relationships  
✅ **Responsive Design**: Mobile-friendly Bootstrap interface  
✅ **Input Validation**: Client and server-side validation  
✅ **Security**: Password hashing and session management  
✅ **Duplicate Prevention**: No duplicate attendance for same date  
✅ **User-Friendly Interface**: Clean, intuitive design  

## Future Enhancements (Major Project)

The system is designed to be easily extended with:

- Face recognition-based attendance
- Student login portal
- Attendance analytics and reports
- CSV/Excel export functionality
- Advanced security features
- Mobile app integration
- Automated notifications

## Academic Compliance

This project meets BCA 5th Semester requirements:
- Demonstrates web development concepts
- Implements database connectivity
- Shows understanding of authentication
- Includes proper documentation
- Ready for academic submission

## Screenshots

The application includes:
- Clean login interface
- Comprehensive admin dashboard
- Intuitive attendance marking
- Detailed attendance records
- Responsive design for all devices

## Support

For any issues or questions regarding this project, please refer to the code comments and documentation provided within the application files.

---

**Note**: This is an academic project designed for educational purposes and minor project submission. The system provides a solid foundation that can be enhanced for major project requirements.