AcadAssist

SYSTEM REQUIREMENTS
- Internet connection is required
- Windows, macOS, or Linux operating system
- Python 3.13 or higher
- 4GB RAM recommended
- 500MB free disk space

INSTALLATION INSTRUCTIONS

Step 1: Install Python
1. Check if Python is already installed:
   -------------------------------------------------------------------------------
   python --version
   -------------------------------------------------------------------------------
   
2. If not installed or using an older version, download Python from:
   https://www.python.org/downloads/
   
3. During installation, make sure to check the "Add Python to PATH" checkbox

Step 2: Set Up the Environment

1. Open Command Prompt (Windows) or Terminal (macOS/Linux)

2. Navigate to the AcadAssist directory:
   -------------------------------------------------------------------------------
   cd c:\path\to\AcadAssist
   -------------------------------------------------------------------------------

3. Create a virtual environment:
   - Windows:
     -------------------------------------------------------------------------------
     python -m venv venv
     -------------------------------------------------------------------------------

   - macOS/Linux:
     -------------------------------------------------------------------------------
     python3 -m venv venv
     -------------------------------------------------------------------------------

4. Activate the virtual environment:
   - Windows:
     -------------------------------------------------------------------------------
     venv\Scripts\activate
     -------------------------------------------------------------------------------

   - macOS/Linux:
     -------------------------------------------------------------------------------
     source venv/bin/activate
     -------------------------------------------------------------------------------
   Your command prompt should now show (venv) at the beginning

Step 3: Install Required Libraries

1. With the virtual environment activated, install all dependencies:
   -------------------------------------------------------------------------------
   pip install -r requirements.txt
   -------------------------------------------------------------------------------

2. Download required NLTK data:
    
   -------------------------------------------------------------------------------
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   -------------------------------------------------------------------------------


**Fix SSL Certificate Issues (macOS) 

1. If you encounter SSL certificate errors on macOS, run the following command:
   -------------------------------------------------------------------------------
   /Applications/Python\ 3.x/Install\ Certificates.command
   -------------------------------------------------------------------------------
   (Replace "3.x" with your Python version, e.g., "3.11")
2. This command updates the SSL certificates used by Python on macOS.

Step 4: Configure Settings

1. Ensure the .env file exists with the following settings:
   -------------------------------------------------------------------------------
   DB_URL=your_postgresql_connection_string
   GOOGLE_API_KEY=your_google_api_key
   HUGGINGFACE_API_KEY=your_huggingface_api_key
   -------------------------------------------------------------------------------

2. Verify that acadassistdrive.json is present for Google Drive integration

RUNNING THE APPLICATION

1. Make sure your virtual environment is activated:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

2. Run the application:
   -------------------------------------------------------------------------------
   python main.py
   -------------------------------------------------------------------------------

3. The login screen will appear, allowing you to sign in as a student or teacher

User Credentials:
- Student: Register a new account through the application's sign-up page
- Teacher: Use pre-configured credentials
  Sample teacher login:
  Email: teacher@acadassist.edu
  Password: AcadTeach_2025

USER GUIDE

User Types

Student Accounts
- Full access to all features
- Can register a new account from the login page
- Can participate in study groups

Teacher Accounts
- Limited to resource management features
- Cannot register through the app (accounts must be pre-configured)
- Can upload and manage resources for students

Feature Guide

1. AI Study Assistant
Purpose: Chat with an AI to get study help and answers to academic questions
Access: Click "AI Study Assistant" in the sidebar menu
How to use:
- Type your study question in the text box at the bottom of the screen
- Press "Send" or hit Enter
- Wait for the AI to generate a response
- Click "New Chat" to start a fresh conversation
Note: Requires internet connection and valid GOOGLE_API_KEY

2. Resource Management
Purpose: Share and access educational materials through Google Drive
Access: Click "Resource Management" in the sidebar menu
How to use:
- For students:
  - View and download resources uploaded by teachers and other students
  - Click "Download" on any resource to save it locally
  - Click "Upload Resource" to add your own materials
- For teachers:
  - Same as students, plus ability to remove resources
  - Click "Remove" on any resource to delete it from the system
Note: Requires internet connection and Google Drive integration

3. Schedule Management
Purpose: Organize academic deadlines and receive reminders
Access: Click "Schedule Management" in the sidebar menu
How to use:
- Select a date on the calendar
- Enter deadline description
- Set deadline time (hour/minute)
- Set reminder time and days before deadline
- Click "Save Deadline" to create and schedule email reminders
Note: Email reminders require internet connection

4. Notes Summarization
Purpose: Automatically generate concise summaries of lengthy notes
Access: Click "Notes Summarization" in the sidebar menu
How to use:
- Paste your text directly into the input box or click "Upload Notes" to import from a file (only .txt files are supported)
- For testing purposes, you can use the sample file 'test.txt' located in the 'dummy_testing' folder
- Click "Summarize Notes" to generate a condensed version
- The summary will appear in the output box below
Note: Works offline after initial NLTK downloads

5. Plagiarism Detection
Purpose: Check content for potential plagiarism
Access: Click "Plagiarism Detection" in the sidebar menu
How to use:
- Choose detection mode:
  - Offline: Compare two texts for similarity
    - Enter the first text in the top box
    - Enter the second text in the bottom box
  - Online: Check text against online content (requires internet)
    - Enter your text in the input box or upload a .txt file
    - For testing purposes, you can use the sample file 'test.txt' located in the 'dummy_testing' folder
- Click "Check for Plagiarism"
- View similarity percentage in the results section
Note: Online mode requires internet connection and HUGGINGFACE_API_KEY

6. Study Group Matcher
Purpose: Find students with similar academic interests
Access: Click "Study Group Matcher" in the sidebar menu
How to use:
- Select your academic interests from the checklist
- Click "Save/Update Interests" to store your preferences
- Click "Find Matching Students" to discover peers with similar interests
- View matching students and their similarity scores in the results list
Note: Requires database connection to work properly

TROUBLESHOOTING

Common Issues and Solutions

Application Doesn't Start
- Ensure Python is installed and in PATH
- Verify virtual environment is activated
- Check if all dependencies are installed:
  -------------------------------------------------------------------------------
  pip install -r requirements.txt
  -------------------------------------------------------------------------------

Database Connection Errors
- Verify DB_URL in .env file
- Check your internet connection
- Ensure PostgreSQL service is running

AI Chatbot Not Working
- Verify GOOGLE_API_KEY in .env file
- Check your internet connection

Plagiarism Detection (Online) Not Working
- Verify HUGGINGFACE_API_KEY in .env file
- Check your internet connection

Google Drive Integration Issues
- Verify acadassistdrive.json exists and has valid credentials
- Check internet connection

NLTK Errors
- Run the NLTK download commands again:
  -------------------------------------------------------------------------------
  python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
  -------------------------------------------------------------------------------

PyQt6 Installation Issues
- Try reinstalling with:
  -------------------------------------------------------------------------------
  pip uninstall PyQt6
  pip install PyQt6
  -------------------------------------------------------------------------------

SSL Certificate Issues (macOS)
- If you encounter SSL certificate errors on macOS, run the following command:
  -------------------------------------------------------------------------------
  /Applications/Python\ 3.x/Install\ Certificates.command
  -------------------------------------------------------------------------------
  (Replace "3.x" with your Python version, e.g., "3.11")
- This command updates the SSL certificates used by Python on macOS

SUPPORT & CONTACT
For assistance, please contact:
- Email: acadassistant8@gmail.com