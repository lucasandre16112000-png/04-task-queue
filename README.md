# ⚙️ Distributed Task Queue System

A robust and professional **asynchronous task queue system** with **Visual Web Dashboard**, demonstrating best practices in distributed systems architecture.

![Dashboard Screenshot](dashboard_screenshot.webp)

---

## 🎯 What is it?

A **task queue system** that:
- ✅ Receives tasks to execute
- ✅ Puts them in a queue for processing
- ✅ Executes them one by one in the background
- ✅ Shows status in real-time
- ✅ Retries if it fails

Commonly used in web applications to process heavy tasks without freezing the interface!

---

## ✨ Features

| Feature | Description |
|:---|:---|
| **Web Dashboard** | Visual interface to create and monitor tasks |
| **5 Task Types** | Email, Report, Image, Synchronization, Cleanup |
| **Real-Time Statistics** | Total, Pending, Processing, Completed, Failed |
| **Success Rate** | Automatic success rate calculation |
| **Execute All Button** | Creates all 5 tasks at once for testing |

---

## 🚀 How to Use (Complete Guide from Zero)

### ⚠️ Requirement: Python 3.8+

**You NEED to have Python installed!**

#### Step 1: Install Python

1. Visit: https://www.python.org/downloads/
2. Download the latest version (3.10 or higher)
3. Run the installer
4. **⚠️ IMPORTANT:** During installation, check the option **"Add Python to PATH"**
5. Click "Install Now"
6. Restart your computer

#### Verify Python is installed:

Open **CMD** or **PowerShell** and type:
```bash
python --version
```

If it shows the version (ex: `Python 3.12.10`), Python is ready! ✓

---

### 📥 Step 1: Download the Project

**Option A - Without Git (Easier):**

1. Visit: https://github.com/lucasandre16112000-png/04-task-queue
2. Click the green **"Code"** button
3. Click **"Download ZIP"**
4. Extract the file to a folder (ex: `C:\Users\[your_username]\Desktop\04-task-queue`)

**Option B - With Git:**

Open PowerShell/CMD and run:
```bash
git clone https://github.com/lucasandre16112000-png/04-task-queue.git
cd 04-task-queue
```

---

### ▶️ Step 2: Run (2 Clicks!)

**Option A - Recommended (Automatic):**

1. Navigate to the project folder
2. **Double-click** on **`TaskQueueLauncher_v2.bat`**
3. Wait a few seconds
4. **Dashboard opens automatically!**

The script will:
- ✅ Check Python
- ✅ Install Flask (if needed)
- ✅ Download project (if needed)
- ✅ Start server
- ✅ Open browser

**Option B - Simple:**

1. Navigate to the project folder
2. **Double-click** on **`INICIAR.bat`**
3. Wait a few seconds
4. **Dashboard opens automatically!**

**Option C - Manual (For Programmers):**

Open PowerShell/CMD in the project folder and run:
```bash
pip install flask
python app.py
```

Then open your browser at: http://localhost:5000

---

### 🌐 Step 3: Access the Dashboard

If the browser doesn't open automatically, open it manually:

```
http://localhost:5000
```

---

## 📊 How to Use the Dashboard

### Create Tasks

Click one of the buttons to create tasks:

| Button | What it does |
|:---|:---|
| 📧 **Send Email** | Simulates email sending |
| 📄 **Generate Report** | Simulates PDF creation |
| 🖼️ **Process Image** | Simulates image filtering |
| 🔄 **Sync Data** | Simulates database synchronization |
| 🧹 **Clean Cache** | Simulates data cleanup |
| ⚡ **Execute All** | Creates all 5 tasks |

### Monitor Tasks

The dashboard shows in real-time:

- **Total** - Total number of tasks created
- **Pending** - Tasks waiting to be processed
- **Processing** - Tasks being executed now
- **Completed** - Tasks finished successfully
- **Failed** - Tasks that failed
- **Success Rate** - Success percentage

---

## 📁 Project Structure

```
04-task-queue/
├── 📜 app.py                    # Flask Server (Backend)
├── 📜 TaskQueueLauncher_v2.bat  # Main executable ⭐
├── 📜 INICIAR.bat               # Simple executable
├── 📜 requirements.txt          # Dependencies
├── 📜 README.md                 # This file
│
├── 📂 templates/
│   └── index.html               # Dashboard interface
│
├── 📂 static/
│   ├── css/style.css            # Visual styles
│   └── js/app.js                # Interactivity
│
└── 📂 (Test files)
    ├── execution_output.txt
    ├── generate_screenshot.py
    └── screenshots/
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|:---|:---|
| **Python 3.8+** | Backend and processing |
| **Flask** | Web server and REST API |
| **HTML5/CSS3** | Visual interface |
| **JavaScript** | Interactivity |
| **Threading** | Asynchronous processing |

---

## ❌ Troubleshooting

### ❌ Error: "Python was not found"

**Solution:**
1. Install Python: https://www.python.org/downloads/
2. **IMPORTANT:** Check "Add Python to PATH" during installation
3. Restart your computer
4. Run the launcher again

### ❌ Error: "Port 5000 is already in use"

**Solution:**
1. Close other programs that might be using port 5000
2. Or edit `app.py` and change `port=5000` to another port (ex: 5001)
3. Save and run again

### ❌ Browser doesn't open automatically

**Solution:**
1. Open your browser manually
2. Visit: http://localhost:5000

### ❌ Error: "No module named 'flask'"

**Solution:**
Open PowerShell/CMD and run:
```bash
pip install flask
```

### ❌ PowerShell permission error

**Solution:**
Open PowerShell as administrator and run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📊 Main Files

| File | Description |
|---------|-----------|
| `TaskQueueLauncher_v2.bat` | ⭐ **Main executable** - With automatic download |
| `INICIAR.bat` | Simple executable - Current folder |
| `app.py` | Flask server |
| `requirements.txt` | Project dependencies |
| `templates/index.html` | Dashboard interface |
| `static/css/style.css` | CSS styles |
| `static/js/app.js` | JavaScript |

---

## 🎓 Quick Summary

**For the client to use:**

1. ✅ Install Python (https://www.python.org/downloads/)
2. ✅ Download the project from GitHub
3. ✅ Double-click `TaskQueueLauncher_v2.bat`
4. ✅ **Done! Everything works automatically!**

---

## 👨‍💻 Author

**Lucas André S**

- GitHub: [@lucasandre16112000-png](https://github.com/lucasandre16112000-png)

---

## 📄 License

This project is under the MIT license.

---

**Developed with ❤️ by Lucas André S**

**Version:** 1.0.0  
**Last update:** January 2026
