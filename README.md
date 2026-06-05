# 📚 E-Library Management System

An online E-Library Management System built using Flask, HTML, CSS, JavaScript, and JSON-based data storage. The system provides separate functionalities for administrators and users to manage library resources efficiently.

## 🚀 Features

### User Features
- User Registration and Login
- Browse Available Books
- View Issued Books
- Personalized Dashboard
- Book Recommendations
- Access Study Materials and Notices

### Admin Features
- Admin Login
- Manage Students
- Manage Programs
- Manage Books
- Approve/Reject User Registrations
- Track Book Issuance
- Manage Library Cards
- Monitor Transactions
- Upload Study Resources

### System Features
- Role-Based Authentication
- Dashboard Analytics
- Secure File Uploads
- JSON-Based Data Management
- Responsive User Interface
- Session Management

## 🛠️ Technologies Used

- Python
- Flask
- HTML5
- CSS3
- JavaScript
- JSON
- Jinja2 Templates
- Gunicorn
- Render (Deployment)

## 📂 Project Structure

```text
e-library/
│
├── app.py
├── requirements.txt
├── data/
│   ├── users.json
│   ├── students.json
│   ├── programs.json
│   ├── transactions.json
│
├── static/
│   ├── css/
│   ├── uploads/
│   ├── images/
│
├── template/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── other templates
│
└── README.md
```

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/e-library.git
cd e-library
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## 🌐 Deployment

The project is deployed using Render.

Deployment Steps:

1. Push project to GitHub.
2. Connect GitHub repository with Render.
3. Set Build Command:

```bash
pip install -r requirements.txt
```

4. Set Start Command:

```bash
gunicorn app:app
```

5. Deploy Web Service.

## 🔒 Authentication

The application uses session-based authentication with separate access control for:

- Admin
- Registered Users

## 📈 Future Enhancements

- Database Integration (SQLite/PostgreSQL)
- Email Verification
- Password Reset System
- Book Search and Filtering
- Fine Management System
- Real-Time Notifications
- Advanced Analytics Dashboard
- Cloud Storage Integration

## 👨‍💻 Author

Ankit Kumar

## 📄 License

This project is developed for educational and academic purposes.
