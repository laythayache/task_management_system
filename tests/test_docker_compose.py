import os
import subprocess
import unittest

class TestDockerCompose(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Ensure that the environment variables are set for testing
        os.environ['POSTGRES_USER'] = 'test_user'
        os.environ['POSTGRES_PASSWORD'] = 'test_password'
        os.environ['POSTGRES_DB'] = 'test_db'
        os.environ['DATABASE_URL'] = 'postgresql://test_user:test_password@db:5432/test_db'
        os.environ['REDIS_URL'] = 'redis://redis:6379'
        os.environ['JWT_SECRET'] = 'test_jwt_secret'

    def test_docker_compose_up(self):
        # Test if docker-compose up runs without errors
        result = subprocess.run(['docker-compose', '-f', 'docker-compose.yml', 'up', '--abort-on-container-exit'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.returncode, 0, msg=f'Docker Compose up failed: {result.stderr.decode()}')

    def test_docker_compose_prod_up(self):
        # Test if docker-compose -prod up runs without errors
        result = subprocess.run(['docker-compose', '-f', 'docker-compose.prod.yml', 'up', '--abort-on-container-exit'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.returncode, 0, msg=f'Docker Compose Prod up failed: {result.stderr.decode()}')

    def test_env_file_exists(self):
        # Test if .env.example file exists
        self.assertTrue(os.path.isfile('.env.example'), '.env.example file does not exist')

    def test_nginx_config_exists(self):
        # Test if nginx.conf file exists
        self.assertTrue(os.path.isfile('nginx.conf'), 'nginx.conf file does not exist')

    def test_env_variables(self):
        # Test if all required environment variables are set
        required_vars = ['POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB', 'DATABASE_URL', 'REDIS_URL', 'JWT_SECRET']
        for var in required_vars:
            self.assertIn(var, os.environ, f'{var} is not set in environment variables')

if __name__ == '__main__':
    unittest.main()