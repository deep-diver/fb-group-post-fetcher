import os
import shutil
import tempfile
from unittest import TestCase

from lib.config.config import Config
from lib.config.dot_env_read_writer import DotEnvReadWriter


class TestDotEnvReadWriter(TestCase):
    def setUp(self) -> None:
        self.env_file_content = """
    FB_GROUP_ID=123
    FB_ACCESS_TOKEN="abc"
    FB_APP_ID=123
    FB_APP_SECRET="123"
    SMTP_USER="smtp_user"
    SMTP_PASS="smtp_pass"
    TOP_K=10
    FIRST_WORDS=10
"""
        self._temp_dir = tempfile.mkdtemp()
        self.env_file_path = os.path.join(self._temp_dir, ".env")

        with open(self.env_file_path, "w") as file:
            file.write(self.env_file_content)

    def tearDown(self) -> None:
        """Deletes a temporary directory"""
        shutil.rmtree(self._temp_dir)

    @staticmethod
    def _get_config() -> Config:
        config = Config()
        config.FB_GROUP_ID = "123"
        config.FB_ACCESS_TOKEN = "abc"
        config.FB_APP_ID = "123"
        config.FB_APP_SECRET = "123"
        config.SMTP_USER = "smtp_user"
        config.SMTP_PASS = "smtp_pass"
        config.TOP_K = 10
        config.FIRST_WORDS = 10

        return config

    def test_read(self):
        env_rw = DotEnvReadWriter(self.env_file_path)
        config = env_rw.read()

        expected = self._get_config()

        self.assertEqual(config, expected)

    def test_write(self):
        env_rw = DotEnvReadWriter(self.env_file_path)
        config = env_rw.read()

        config.FB_ACCESS_TOKEN = "I changed FB_ACCESS_TOKEN"

        self.assertTrue(env_rw.write(config))

        new_env_rw = DotEnvReadWriter(self.env_file_path)
        new_config = new_env_rw.read()

        self.assertEqual(new_config, config)

