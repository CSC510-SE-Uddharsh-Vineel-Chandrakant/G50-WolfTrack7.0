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
        cls.conn = sqlite3.connect(cls.db)
        cls.cursor = cls.conn.cursor()

    def setUp(self):
        # Clear the database tables before each test
        self.cursor.execute("DELETE FROM client")
        self.cursor.execute("DELETE FROM jobs")
        self.cursor.execute("DELETE FROM resumes")
        self.conn.commit()

    def tearDown(self):
        pass  # Connection remains open during all tests

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()  # Close the connection after all tests are done
        conn = sqlite3.connect(cls.db)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS client")
        cursor.execute("DROP TABLE IF EXISTS jobs")
        cursor.execute("DROP TABLE IF EXISTS resumes")
        conn.commit()
        conn.close()

    def test_add_client(self):
        client_data = ('John Doe', 'johndoe', 'password123', 'user')
        dbutils.add_client(client_data, self.db)
        result = dbutils.find_user('johndoe', self.db)
        self.assertIsNotNone(result)
        self.assertEqual(result[1], 'John Doe')

    def test_get_user_by_username_role(self):
        client_data = ('Alice Smith', 'alicesmith', 'password789', 'admin')
        dbutils.add_client(client_data, self.db)
        result = dbutils.get_user_by_username_role('alicesmith', 'admin', self.db)
        self.assertIsNotNone(result)
        self.assertEqual(result[1], 'Alice Smith')

    def test_add_job(self):
        job_data = ('CompanyX', 'LocationY', 'PositionZ', 50000, 'Open')
        dbutils.add_job(job_data, self.db)
        result = dbutils.get_job_applications_by_status(self.db, 'Open')
        self.assertTrue(any(job[1] == 'CompanyX' for job in result))

    def test_update_job_application_by_id(self):
        job_data = ('CompanyY', 'LocationZ', 'PositionW', 55000, 'Open')
        dbutils.add_job(job_data, self.db)

        result = dbutils.get_job_applications_by_status(self.db, 'Open')
        job_id = result[0][0]
        dbutils.update_job_application_by_id(job_id, 'UpdatedCompany', 'UpdatedLocation', 'UpdatedPosition', 70000, 'Closed', self.db)

        updated_result = dbutils.get_job_applications_by_status(self.db, 'Closed')
        self.assertTrue(any(job[1] == 'UpdatedCompany' for job in updated_result))

    def test_delete_job_application_by_job_id(self):
        job_data = ('CompanyZ', 'LocationX', 'PositionY', 40000, 'Open')
        dbutils.add_job(job_data, self.db)

        result = dbutils.get_job_applications_by_status(self.db, 'Open')
        job_id = result[0][0]
        dbutils.delete_job_application_by_job_id(job_id, self.db)

        updated_result = dbutils.get_job_applications_by_status(self.db, 'Open')
        self.assertFalse(any(job[1] == 'CompanyZ' for job in updated_result))

    def test_get_resumes_by_user_name(self):
        user_name = 'janedoe'
        file_name = 'resume.pdf'
        dbutils.add_client(('Jane Doe', user_name, 'password123', 'user'), self.db)
        dbutils.save_resume_metadata(user_name, file_name, 'PositionA', self.db)

        result = dbutils.get_resumes_by_user_name(user_name, self.db)
        self.assertTrue(any(resume[2] == file_name for resume in result))
        

    def test_save_resume_metadata_success(self):
    # Arrange: Add a client to associate the resume with
        user_name = 'janedoe'
        file_name = 'resume.pdf'
        position = 'Software Engineer'
        dbutils.add_client(('Jane Doe', user_name, 'password123', 'user'), self.db)

    # Act: Save resume metadata
        dbutils.save_resume_metadata(user_name, file_name, position, self.db)

    # Assert: Verify that the resume metadata was saved correctly
        result = dbutils.get_resumes_by_user_name(user_name, self.db)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], user_name)  # Username matches
        self.assertEqual(result[0][2], file_name)  # File name matches
        self.assertEqual(result[0][3], position)   # Position matches




if __name__ == '__main__':
    unittest.main()


