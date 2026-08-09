import unittest
import json
import io
import os
import sys

# Ensure the root project directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class TestV2Pipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.user_id = None
        cls.session_jwt = None
        cls.analysis_id = None

    def test_01_auth(self):
        print("\n--- Testing Step 1: Auth ---")
        response = self.client.post('/api/v2/users/auth', json={
            'provider': 'test_provider',
            'token': 'test_token_123'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('user_id', data)
        self.assertIn('session_jwt', data)
        TestV2Pipeline.user_id = data['user_id']
        TestV2Pipeline.session_jwt = data['session_jwt']
        print(f"Auth Success! User ID: {self.user_id}")

    def test_02_analyze(self):
        print("\n--- Testing Step 2: Analyze ---")
        # Create a minimal PDF
        pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n4 0 obj\n<< /Length 64 >>\nstream\nBT\n/F1 12 Tf\n10 700 Td\n(Python Flask Docker Kubernetes Redis) Tj\nET\nendstream\nendobj\n5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\ntrailer\n<< /Size 6 /Root 1 0 R >>\n%%EOF"
        
        data = {
            'resume': (io.BytesIO(pdf_content), 'resume.pdf'),
            'job_description': 'Looking for Python, Flask, Machine Learning, and AWS skills.',
            'target_branch': 'Software Engineering'
        }
        
        headers = {
            'Authorization': f"Bearer {TestV2Pipeline.session_jwt}"
        }
        
        import contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            response = self.client.post('/api/v2/analyze', data=data, headers=headers, content_type='multipart/form-data')
            
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        
        self.assertIn('analysis_id', json_data)
        self.assertIn('overall_score', json_data)
        self.assertIn('skills_found', json_data)
        self.assertIn('skills_missing', json_data)
        self.assertIn('roadmap', json_data)
        
        TestV2Pipeline.analysis_id = json_data['analysis_id']
        print(f"Analyze Success! Score: {json_data['overall_score']}, Analysis ID: {self.analysis_id}")

    def test_03_history(self):
        print("\n--- Testing Step 3: History ---")
        headers = {
            'Authorization': f"Bearer {TestV2Pipeline.session_jwt}"
        }
        response = self.client.get(f'/api/v2/users/{TestV2Pipeline.user_id}/history', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertIn('history', data)
        self.assertTrue(len(data['history']) > 0)
        
        # Verify our specific analysis is in there
        analysis_ids = [item['analysis_id'] for item in data['history']]
        self.assertIn(TestV2Pipeline.analysis_id, analysis_ids)
        print("History Success! Analysis record found.")

    def test_04_interview(self):
        print("\n--- Testing Step 4: Interview Generate ---")
        headers = {
            'Authorization': f"Bearer {TestV2Pipeline.session_jwt}"
        }
        response = self.client.post('/api/v2/interview/generate', json={
            'analysis_id': TestV2Pipeline.analysis_id,
            'difficulty': 'Intermediate'
        }, headers=headers)
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertIn('questions', data)
        self.assertIn('suggested_answers', data)
        self.assertEqual(len(data['questions']), 5)
        self.assertEqual(len(data['suggested_answers']), 5)
        print("Interview Success! 5 questions generated.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
