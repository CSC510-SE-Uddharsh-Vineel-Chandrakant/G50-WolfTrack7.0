import unittest
import sys
sys.path.append('./')
from unittest.mock import MagicMock, patch
import sqlite3
import dbutils


class TestDBUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = 'test_database.db'
        dbutils.create_tables(cls.db)

    @classmethod
    def tearDownClass(cls):
        conn = sqlite3.connect(cls.db)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS client")
        cursor.execute("DROP TABLE IF EXISTS jobs")
        conn.commit()
        conn.close()

    def test_create_tables(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='client'")
        client_table = cursor.fetchone()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='jobs'")
        jobs_table = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(client_table)
        self.assertIsNotNone(jobs_table)

    def test_add_client(self):
        client_data = ('John Doe', 'johndoe', 'password123', 'user')
        dbutils.add_client(client_data, self.db)
        result = dbutils.find_user('johndoe', self.db)
        self.assertIsNotNone(result)
        self.assertEqual(result[1], 'John Doe')

    def test_find_user(self):
        client_data = ('Jane Doe', 'janedoe', 'password456', 'user')
        dbutils.add_client(client_data, self.db)
        result = dbutils.find_user('janedoe', self.db)
        self.assertIsNotNone(result)
        self.assertEqual(result[1], 'Jane Doe')

    def test_get_user_by_username_role(self):
        # Add a client for testing
        client_data = ('Alice Smith', 'alicesmith', 'password789', 'admin')
        dbutils.add_client(client_data, self.db)
        
        # Fetch the client by username and role
        result = dbutils.get_user_by_username_role('alicesmith', 'admin', self.db)
        
        # Assert that the result is not None and data matches
        self.assertIsNotNone(result)
        self.assertEqual(result[1], 'Alice Smith')
        self.assertEqual(result[3], 'password789')
        self.assertEqual(result[4], 'admin')
        
    """
    def test_add_job(self):
        job_data = ('CompanyX', 'LocationY', 'PositionZ', 50000, 'Open', 'Jane Doe')
        dbutils.add_job(job_data, self.db)
        result = dbutils.get_job_applications(self.db)
        self.assertIsNotNone(result)
        self.assertEqual(result[0][1], 'CompanyX')
    """
    """
    def test_get_job_applications(self):
        result = dbutils.get_job_applications(self.db)
        self.assertIsNotNone(result)
        self.assertTrue(len(result) >= 0)
    """
    """
    def test_update_job_application_by_id(self):
        job_data = ('CompanyX', 'UpdatedLocation', 'UpdatedPosition', 60000, 'Closed')
        dbutils.update_job_application_by_id(*job_data, self.db)
        result = dbutils.get_job_applications(self.db)
        updated_job = [job for job in result if job[1] == 'CompanyX']
        self.assertIsNotNone(updated_job)
        self.assertEqual(updated_job[0][1:], job_data)
    """
    """
    def test_delete_job_application_by_company(self):
        dbutils.delete_job_application_by_company('UpdatedCompany', self.db)
        result = dbutils.get_job_applications(self.db)
        deleted_job = [job for job in result if job[1] == 'UpdatedCompany']
        self.assertEqual(len(deleted_job), 0)
    """
    # def test_get_job_applications_by_status(self):
    #     job_data = ('CompanyA', 'LocationX', 'PositionY', 40000, 'Open')
    #     dbutils.add_job(job_data, self.db)
    #     job_data_closed = ('CompanyB', 'LocationX', 'PositionY', 45000, 'Closed')
    #     dbutils.add_job(job_data_closed, self.db)
        
    #     result_open = dbutils.get_job_applications_by_status(self.db, 'Open')
    #     result_closed = dbutils.get_job_applications_by_status(self.db, 'Closed')
        
    #     self.assertTrue(len(result_open) > 0)
    #     self.assertTrue(len(result_closed) > 0)
    #     self.assertEqual(result_open[0][-1], 'Open')
    #     self.assertEqual(result_closed[0][-1], 'Closed')
    """
    def test_update_job_application_invalid_id(self):
        job_data = ('InvalidCompany', 'UpdatedLocation', 'UpdatedPosition', 60000, 'Closed')
        dbutils.update_job_application_by_id(*job_data, self.db)
        result = dbutils.get_job_applications(self.db)
        updated_job = [job for job in result if job[1] == 'InvalidCompany']
        self.assertEqual(len(updated_job), 0)
    """
    """
    def test_delete_nonexistent_job_application(self):
        dbutils.delete_job_application_by_company('NonexistentCompany', self.db)
        result = dbutils.get_job_applications(self.db)
        deleted_job = [job for job in result if job[1] == 'NonexistentCompany']
        self.assertEqual(len(deleted_job), 0)
    """
    def test_add_new_job(self):
        job_title = 'Software Engineer'
        company_name = 'TechCorp'
        location = 'San Francisco'
        salary = 120000
        status = 'Open'
        job_id = dbutils.add_new_job(job_title, company_name, location, salary, status, self.db)
        
        self.assertIsNotNone(job_id)
        
        job = dbutils.get_job_by_id(job_id, self.db)
        self.assertIsNotNone(job)
        self.assertEqual(job[0], company_name)
        self.assertEqual(job[1], location)
        self.assertEqual(job[2], job_title)
        self.assertEqual(job[3], salary)
        self.assertEqual(job[4], status)

    def test_get_all_jobs(self):
        job1 = ('Software Engineer', 'TechCorp', 'San Francisco', 120000, 'Open')
        job2 = ('Data Scientist', 'DataCorp', 'New York', 110000, 'Closed')
        
        dbutils.add_new_job(*job1, self.db)
        dbutils.add_new_job(*job2, self.db)
        
        jobs = dbutils.get_all_jobs(self.db)
        
        self.assertTrue(len(jobs) >= 2)
        
        job_titles = [job['job_position'] for job in jobs]
        self.assertIn('Software Engineer', job_titles)
        self.assertIn('Data Scientist', job_titles)

    def test_get_job_by_id(self):
        job_title = 'Product Manager'
        company_name = 'ProductCorp'
        location = 'Seattle'
        salary = 130000
        status = 'Open'
        job_id = dbutils.add_new_job(job_title, company_name, location, salary, status, self.db)
        

        job = dbutils.get_job_by_id(job_id, self.db)
        self.assertIsNotNone(job)
        self.assertEqual(job[0], company_name)
        self.assertEqual(job[1], location)
        self.assertEqual(job[2], job_title)
        self.assertEqual(job[3], salary)
        self.assertEqual(job[4], status)
    
    def test_get_job_by_details(self):
        job_title = 'QA Engineer'
        company_name = 'QualityCorp'
        location = 'Austin'
        salary = 90000
        status = 'Open'
        dbutils.add_new_job(job_title, company_name, location, salary, status, self.db)
        

        job = dbutils.get_job_by_details(job_title, company_name, location, salary, status, self.db)
        self.assertIsNotNone(job)
        self.assertEqual(job[1], job_title)
        self.assertEqual(job[2], company_name)
        self.assertEqual(job[3], location)
        self.assertEqual(job[4], salary)
        self.assertEqual(job[5], status)

    def test_get_job_by_id_invalid_id(self):
        job = dbutils.get_job_by_id(9999, self.db)
        self.assertIsNone(job)
    
    def test_get_job_by_details_no_match(self):
        job = dbutils.get_job_by_details('Nonexistent Job', 'NoCompany', 'Nowhere', 0, 'Closed', self.db)
        self.assertIsNone(job)
    
    def test_update_job_application_by_id(self):
        job_title = 'Backend Developer'
        company_name = 'WebTech'
        location = 'Boston'
        salary = 100000
        status = 'Open'
        job_id = dbutils.add_new_job(job_title, company_name, location, salary, status, self.db)
        
        new_company_name = 'WebTech Solutions'
        new_location = 'Cambridge'
        new_job_position = 'Senior Backend Developer'
        new_status = 'Closed'
        dbutils.update_job_application_by_id(job_id, new_company_name, new_location, new_job_position, new_status, self.db)
        

        job = dbutils.get_job_by_id(job_id, self.db)
        self.assertIsNotNone(job)
        self.assertEqual(job[0], new_company_name)
        self.assertEqual(job[1], new_location)
        self.assertEqual(job[2], new_job_position)
        self.assertEqual(job[4], new_status) 
    
    def test_delete_job_application_by_job_id(self):
        job_title = 'Frontend Developer'
        company_name = 'DesignCorp'
        location = 'Miami'
        salary = 90000
        status = 'Open'
        job_id = dbutils.add_new_job(job_title, company_name, location, salary, status, self.db)
        
        dbutils.delete_job_application_by_job_id(job_id, self.db)
    
        job = dbutils.get_job_by_id(job_id, self.db)
        self.assertIsNone(job)
    
    def test_get_job_applications_by_status(self):
        job1 = ('DevOps Engineer', 'CloudCorp', 'San Jose', 115000, 'Open')
        job2 = ('System Administrator', 'ITCorp', 'Dallas', 85000, 'Closed')
        job3 = ('Database Administrator', 'DataCorp', 'Chicago', 95000, 'Open')
        
        dbutils.add_new_job(*job1, self.db)
        dbutils.add_new_job(*job2, self.db)
        dbutils.add_new_job(*job3, self.db)
        
        open_jobs = dbutils.get_job_applications_by_status(self.db, 'Open')
        self.assertTrue(len(open_jobs) >= 2)
        for job in open_jobs:
            self.assertEqual(job[5], 'Open')
        
        closed_jobs = dbutils.get_job_applications_by_status(self.db, 'Closed')
        self.assertTrue(len(closed_jobs) >= 1)
        for job in closed_jobs:
            self.assertEqual(job[5], 'Closed')
    
    def test_save_resume_metadata_and_get_resumes_by_user_name(self):
        client_data = ('Charlie Brown', 'charlie', 'snoopy', 'user')
        dbutils.add_client(client_data, self.db)
    
        user_name = 'charlie'
        file_name = 'resume_charlie.pdf'
        position = 'Graphic Designer'
        dbutils.save_resume_metadata(user_name, file_name, position, self.db)
        
        resumes = dbutils.get_resumes_by_user_name(user_name, self.db)
        self.assertTrue(len(resumes) >= 1)
        self.assertEqual(resumes[0][1], user_name)
        self.assertEqual(resumes[0][2], file_name)
        self.assertEqual(resumes[0][3], position)
    
    def test_update_job_application_by_invalid_id(self):
        invalid_job_id = 9999
        company_name = 'NoCompany'
        location = 'Nowhere'
        job_position = 'NoPosition'
        status = 'Closed'
        dbutils.update_job_application_by_id(invalid_job_id, company_name, location, job_position, status, self.db)
        
        job = dbutils.get_job_by_id(invalid_job_id, self.db)
        self.assertIsNone(job)
    
    def test_delete_job_application_by_invalid_id(self):
        invalid_job_id = 9999
        dbutils.delete_job_application_by_job_id(invalid_job_id, self.db)
        
        job = dbutils.get_job_by_id(invalid_job_id, self.db)
        self.assertIsNone(job)

    def test_save_multiple_resumes_for_user(self):
        client_data = ('Tom Hanks', 'tomh', 'forestgump', 'user')
        dbutils.add_client(client_data, self.db)
        
        user_name = 'tomh'
        file_name1 = 'resume_tom1.pdf'
        file_name2 = 'resume_tom2.pdf'
        position1 = 'Actor'
        position2 = 'Director'
        
        dbutils.save_resume_metadata(user_name, file_name1, position1, self.db)
        dbutils.save_resume_metadata(user_name, file_name2, position2, self.db)
        
        resumes = dbutils.get_resumes_by_user_name(user_name, self.db)
        self.assertEqual(len(resumes), 2)
        file_names = [resume[2] for resume in resumes]
        self.assertIn(file_name1, file_names)
        self.assertIn(file_name2, file_names)

    def test_add_multiple_clients_and_verify_count(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM client")
        initial_count = cursor.fetchone()[0]
        conn.close()
        
        client_data1 = ('Client One', 'clientone', 'password1', 'user')
        client_data2 = ('Client Two', 'clienttwo', 'password2', 'user')
        client_data3 = ('Client Three', 'clientthree', 'password3', 'user')
        dbutils.add_client(client_data1, self.db)
        dbutils.add_client(client_data2, self.db)
        dbutils.add_client(client_data3, self.db)
        
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM client")
        updated_count = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(updated_count, initial_count + 3)

    def test_add_multiple_jobs_and_verify_count(self):
        initial_jobs = dbutils.get_all_jobs(self.db)
        initial_count = len(initial_jobs)
        
        job1 = ('Role One', 'Company One', 'Location One', 50000, 'Open')
        job2 = ('Role Two', 'Company Two', 'Location Two', 60000, 'Open')
        job3 = ('Role Three', 'Company Three', 'Location Three', 70000, 'Open')
        dbutils.add_new_job(*job1, self.db)
        dbutils.add_new_job(*job2, self.db)
        dbutils.add_new_job(*job3, self.db)
        
        updated_jobs = dbutils.get_all_jobs(self.db)
        updated_count = len(updated_jobs)
        
        self.assertEqual(updated_count, initial_count + 3)

    def test_add_job_with_special_characters(self):
        job_title = 'Développeur Sénior'
        company_name = 'Entreprise Étrangère'
        location = 'Montréal'
        salary = 80000
        status = 'Open'
        job_id = dbutils.add_new_job(job_title, company_name, location, salary, status, self.db)
        
        self.assertIsNotNone(job_id)
        
        job = dbutils.get_job_by_id(job_id, self.db)
        self.assertIsNotNone(job)
        self.assertEqual(job[0], company_name)
        self.assertEqual(job[1], location)
        self.assertEqual(job[2], job_title)
        self.assertEqual(job[3], salary)
        self.assertEqual(job[4], status)

    def test_add_job_with_long_fields(self):
        job_title = 'Senior Software Engineer with extensive experience in cloud computing, microservices, and distributed systems'
        company_name = 'Very Large Corporation with International Presence and Multiple Business Units'
        location = 'Remote Position, Open to Global Candidates Across Different Time Zones'
        salary = 150000
        status = 'Open'
        job_id = dbutils.add_new_job(job_title, company_name, location, salary, status, self.db)
        
        self.assertIsNotNone(job_id)
        
        job = dbutils.get_job_by_id(job_id, self.db)
        self.assertIsNotNone(job)
        self.assertEqual(job[0], company_name)
        self.assertEqual(job[1], location)
        self.assertEqual(job[2], job_title)
        self.assertEqual(job[3], salary)
        self.assertEqual(job[4], status)

    def test_add_client_with_special_characters(self):
        client_data = ('José Álvarez', 'josé@álvarez', 'password123', 'user')
        dbutils.add_client(client_data, self.db)
        result = dbutils.find_user('josé@álvarez', self.db)
        self.assertIsNotNone(result)
        self.assertEqual(result[1], 'José Álvarez')

    def test_add_job_with_negative_salary(self):
        job_title = 'Junior Developer'
        company_name = 'StartUp Inc.'
        location = 'New York'
        salary = -50000
        status = 'Open'
        job_id = dbutils.add_new_job(job_title, company_name, location, salary, status, self.db)
        self.assertIsNotNone(job_id)
        job = dbutils.get_job_by_id(job_id, self.db)
        self.assertIsNotNone(job)
        self.assertEqual(job[3], salary)

    def test_job_count_decreases_after_deletion(self):
        initial_jobs = dbutils.get_all_jobs(self.db)
        initial_count = len(initial_jobs)

        job_title = 'Data Analyst'
        company_name = 'DataCorp'
        location = 'Boston'
        salary = 85000
        status = 'Open'
        job_id = dbutils.add_new_job(job_title, company_name, location, salary, status, self.db)

        jobs_after_addition = dbutils.get_all_jobs(self.db)
        self.assertEqual(len(jobs_after_addition), initial_count + 1)

        dbutils.delete_job_application_by_job_id(job_id, self.db)

        jobs_after_deletion = dbutils.get_all_jobs(self.db)
        self.assertEqual(len(jobs_after_deletion), initial_count)

if __name__ == '__main__':
    unittest.main()