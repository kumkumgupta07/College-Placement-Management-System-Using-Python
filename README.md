🎓 College Placement Management System

A **College Placement Management System** built with **Python (Streamlit)** and **MongoDB Atlas** for database storage.  
This system manages **Students, Companies, and College Admins** with separate dashboards, resume analyzer, and cross-notification features.  

---

## 🚀 Features
- 🔐 **User Authentication** (Login/Register with MongoDB Atlas)
- 🎓 **Student Dashboard**: Apply for jobs, upload resumes, track status
- 🏢 **Company Dashboard**: Post jobs, analyze resumes (ATS scoring), shortlist candidates
- 🏫 **College Dashboard**: Monitor students & company interactions
- 📑 **Resume Analyzer**: Upload resume & get ATS score vs job description
- 🔔 **Cross-Dashboard Notifications**:
  - Company posts job → Students & College notified
  - Student applies → Company & College notified
  - Resume stored for future analysis

---

## 🛠️ Technologies Used
- **Frontend/UI**: Streamlit (Python-based)
- **Backend**: Python
- **Database**: MongoDB Atlas (Cloud NoSQL)
- **Libraries**:
  - `streamlit`
  - `pymongo`
  - `python-dotenv`
  - `reportlab` (for PDFs)
  - `pandas`
  - `numpy`

 📂 Project Structure
project/
│── app.py # Main entry point
│── student/
│ └── dashboard.py # Student dashboard
│── company/
│ └── dashboard.py # Company dashboard
│── college/
│ └── dashboard.py # College dashboard
│── utils/
│ ├── database.py # MongoDB connection
│ ├── session.py # Session management
│ └── file_utils.py # File handling
│── requirements.txt # Python dependencies
│── .env # Environment variables (not pushed to GitHub)
│── .gitignore # Ignore .env and caches
│── README.md # Project documentation



---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/college-placement-system.git
cd college-placement-system\


Install Dependencies
pip install -r requirements.txt
