#!/usr/bin/env python3
import unittest
from api import create_app, db
from api.models.models import User, Organisation
from flask_jwt_extended import create_access_token, decode_token
from datetime import timedelta


class TestToken(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.pvznacjzdmfuitexpnzp:xender2022$@aws-0-eu-central-1.pooler.supabase.com:6543/postgres'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_token_expiration(self):
        # Register a user
        self.client.post('/auth/register', json={
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john@example.com',
            'password': 'password',
            'phone': '1234567890'
        })

        # Log the user in
        response = self.client.post('/auth/login', json={
            'email': 'john@example.com',
            'password': 'password'
        })

        data = response.get_json()
        access_token = data['data']['accessToken']
        decoded_token = decode_token(access_token)
        
        # Verify token expiration
        expiration_time = decoded_token['exp']
        current_time = time.time()
        self.assertAlmostEqual(expiration_time, current_time + 3600, delta=5)


class OrganisationAccessTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.pvznacjzdmfuitexpnzp:xender2022$@aws-0-eu-central-1.pooler.supabase.com:6543/postgres'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            self.res = self.client.post('/auth/register', json={
                'firstName': 'John',
                'lastName': 'Doe',
                'email': 'john@example.com',
                'password': 'password',
                'phone': '1234567890'
            })
            print(self.res)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_reg(self):
        self.assertEqual(self.res.status_code, 201)
        self.assertIn('accessToken', self.res.json['data'])
        self.assertEqual(self.res.json['data']['user']['firstName'], 'John')
        self.assertEqual(self.res.json['data']['user']['email'], 'john@example.com')

        # test users is registered successfuly when no org is specified
        usr = User.query.filter_by(name = self.user1.first_name).first()
        self.assertIsNotNone(usr)

        # test default org is created
        org = Organisation.query.filter_by(name = "John's Organisation").first()
        self.assertIsNotNone(org)

    def test_successful_login(self):
        response = self.client.post('/auth/login', json={
            'email': 'john@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('accessToken', response.json['data'])
        self.assertEqual('john@example.com', response.json['data']['user']['email'])

    def test_invalid_login_credentials(self):
        response = self.client.post('/auth/login', json={
            'email': 'john@example.com',
            'password': 'wrong'
        })
        self.assertEqual(response.status_code, 401)

    def test_missing_required_fields(self):
        response = self.client.post('/auth/register', json={
            'lastName': 'Doe',
            'email': 'john@example.com',
            'password': 'password',
            'phone': '1234567890'
        })
        self.assertEqual(response.status_code, 422)
        self.assertIn('errors', response.json)

    def test_duplicate_email(self):
        response = self.client.post('/auth/register', json={
            'firstName': 'Julye',
            'lastName': 'Jane',
            'email': 'john@example.com',
            'password': 'password',
            'phone': '0987654321'
        })
        self.assertEqual(response.status_code, 422)
        self.assertIn('errors', response.res.json)


if __name__ == '__main__':
    unittest.main()