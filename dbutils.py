'''
MIT License

Copyright (c) 2023 Shonil B, Akshada M, Rutuja R, Sakshi B

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import sqlite3
import os


def create_tables(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")  # Enable WAL for concurrent access
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS client (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            usertype TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            location TEXT,
            job_position TEXT,
            salary INTEGER,
            status TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            fileName TEXT NOT NULL,
            position TEXT,
            UNIQUE(username, fileName),
            FOREIGN KEY(username) REFERENCES client(username)
        )
    ''')
    conn.commit()
    conn.close()

def add_client(value_set,db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    print(value_set)
    # Inserting rows into the 'client' table
    cursor.execute("INSERT INTO client (name, username, password, usertype) VALUES (?, ?, ?, ?)",
                       value_set)
    conn.commit()
    conn.close()

def get_user_by_username_role(username, usertype, db):
    conn = sqlite3.connect(db)
    print('Data==>', username, usertype)
    cursor = conn.cursor()
    # Querying the 'client' table
    cursor.execute("SELECT * FROM client WHERE username = ? AND usertype=?", (username,usertype))
    rows = cursor.fetchone()
    conn.close()
    return rows


def find_user(data,db):
    conn = sqlite3.connect(db)
    print('Data==>', data)
    cursor = conn.cursor()
    # Querying the 'client' table
    cursor.execute("SELECT * FROM client where username ='"+str(data)+"'")
    rows = cursor.fetchone()
    conn.close()
    print('rowsss->>>', rows)
    return rows


def add_job(data,db):
    conn = sqlite3.connect(db)
    print('Data==>', data)
    cursor = conn.cursor()
    # Inserting rows into the 'jobs' table
    cursor.execute("INSERT INTO jobs (company_name, location, job_position, salary, status, user_name) VALUES (?, ?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

def get_job_applications(user_name, db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE user_name=?",(user_name,))
    rows = cursor.fetchall()  # Use fetchall() to get all rows
    conn.close()
    return rows

def add_job_for_user(company_name, location, job_position, user_name,salary,status, db):
    """
    Add a job application for a specific user.

    :param company_name: Name of the company.
    :param location: Job location.
    :param job_position: Position applied for.
    :param salary: Salary offered.
    :param status: Status of the job application (e.g., Open, Closed).
    :param user_name: Username of the user associated with the job application.
    :param db: Path to the SQLite database.
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        # Insert job data with the associated username
        cursor.execute("""
            INSERT INTO jobs (company_name, location, job_position, user_name,salary,status)
            VALUES (?, ?, ?, ?,?,?);
        """, (company_name, location, job_position, user_name,salary,status))
        conn.commit()
        print(f"Job added successfully for user: {user_name}")
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
        raise
    finally:
        conn.close()

def update_job_application_by_id(job_id, company, location, jobposition, status,db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Update the 'jobs' table based on jobid
    cursor.execute("UPDATE jobs SET company_name=?, location=?, job_position=?, status=? WHERE id=?",
                   (company, location, jobposition, status, job_id))

    conn.commit()
    conn.close()


def delete_job_application_by_job_id(job_id,db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Delete the job application from the 'jobs' table based on the company name
    cursor.execute("DELETE FROM jobs WHERE id=?", (job_id,))

    conn.commit()
    conn.close()

def get_job_applications_by_status(db, status):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE status = ?", (status,))
    rows = cursor.fetchall()  # Use fetchall() to get all rows
    conn.close()
    print('rows ->>>', rows)
    return rows

def get_resumes_by_user_name(user_name, db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables:", tables)
    db_path = os.path.abspath(db)
    print(f"Connecting to database: {db_path}")

    cursor.execute("SELECT * FROM resumes WHERE username = ?", (user_name,))
    rows = cursor.fetchall()  # Use fetchall() to get all rows
    conn.close()
    print('rows ->>>', rows)
    return rows

def save_resume_metadata(user_name, file_name, position, db_path):
    """
    Save resume metadata into the database.

    :param user_name: Username of the uploader.
    :param file_name: Name of the uploaded file.
    :param position: Position associated with the resume (optional).
    :param db_path: Path to the SQLite database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()


    try:
        # Insert the resume metadata
        cursor.execute("""
            INSERT INTO resumes (username, fileName, position)
            VALUES (?, ?, ?);
        """, (user_name, file_name, position))
        conn.commit()
        print(f"Resume metadata for {file_name} saved successfully.")
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def get_all_jobs(db):
    """
    Fetch all jobs from the database.

    :param db: Path to the SQLite database.
    :return: List of all jobs with their details.
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, company_name, location, job_position, salary, status 
        FROM jobs
    """)
    jobs = cursor.fetchall()
    conn.close()

    # Convert jobs to a list of dictionaries for JSON response
    return [
        {
            "id": job[0],
            "company_name": job[1],
            "location": job[2],
            "job_position": job[3],
            "salary": job[4],
            "status": job[5]
        }
        for job in jobs
    ]


def get_job_by_id(job_id, db):
    """
    Fetch job details by job ID.

    :param job_id: ID of the job.
    :param db: Path to the SQLite database.
    :return: Tuple containing job details (company_name, location, job_position, salary, status).
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT company_name, location, job_position, salary, status
        FROM jobs WHERE id = ?
    """, (job_id,))
    job = cursor.fetchone()
    conn.close()
    return job

def get_job_by_details(job_title, company_name, location,salary,status, db):
    """
    Fetch a job by its details (title, company, location).

    :param job_title: Job title.
    :param company_name: Company name.
    :param location: Job location.
    :param db: Path to the SQLite database.
    :return: Tuple containing job details if found, else None.
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, job_position, company_name, location, salary,status 
        FROM jobs WHERE job_position = ? AND company_name = ? AND location = ? AND salary = ? AND status = ?
    """, (job_title, company_name, location,salary,status))
    job = cursor.fetchone()
    conn.close()
    return job


def add_new_job(job_title, company_name, location,salary,status, db):
    """
    Add a new job to the jobs table.

    :param job_title: Job title.
    :param company_name: Name of the company.
    :param location: Job location.
    :param salary: Job salary.
    :param contract_type: Contract type (e.g., Full-time, Part-time).
    :param contract_time: Contract time (e.g., Permanent, Temporary).
    :param description: Job description.
    :param db: Path to the SQLite database.
    :return: ID of the newly inserted job.
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO jobs (job_position, company_name, location,salary,status)
            VALUES (?, ?, ?,?,?)
        """, (job_title, company_name, location,salary,status))
        conn.commit()
        return cursor.lastrowid  # Return the auto-incremented ID of the new job
    finally:
        conn.close()
