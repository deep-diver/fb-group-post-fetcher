import logging
from typing import Tuple

import dotenv

from lib.config.base_config_read_writer import AbstractConfigReadWriter
from lib.config.config import Config


class DotEnvReadWriter(AbstractConfigReadWriter):
    def __init__(self, env_file: str):
        self.env_file = env_file

    def read(self) -> Config:
        """Returns Config from self.env_file"""
        dotenv_values = dotenv.dotenv_values(self.env_file)
        return Config.of(**dotenv_values)

    @staticmethod
    def log_on_fail(dotenv_result: Tuple[bool, str, str]) -> bool:
        ok, key, val = dotenv_result

        if not ok:
            logging.warning(
                "failed to update .env value (key = %s, value = %s)", key, val
            )

        return ok

    def write(self, config: Config) -> bool:
        """Writes Config to .env and returns True if all write succeed"""
        ok = True

        ok &= self.log_on_fail(
            dotenv.set_key(self.env_file, "FB_GROUP_ID", config.FB_GROUP_ID)
        )
        ok &= self.log_on_fail(
            dotenv.set_key(self.env_file, "FB_GROUP_ID", config.FB_GROUP_ID)
        )
        ok &= self.log_on_fail(
            dotenv.set_key(self.env_file, "FB_ACCESS_TOKEN", config.FB_ACCESS_TOKEN)
        )
        ok &= self.log_on_fail(
            dotenv.set_key(self.env_file, "FB_APP_ID", config.FB_APP_ID)
        )
        ok &= self.log_on_fail(
            dotenv.set_key(self.env_file, "FB_APP_SECRET", config.FB_APP_SECRET)
        )

        ok &= self.log_on_fail(
            dotenv.set_key(self.env_file, "SMTP_USER", config.SMTP_USER)
        )
        ok &= self.log_on_fail(
            dotenv.set_key(self.env_file, "SMTP_PASS", config.SMTP_PASS)
        )

        ok &= self.log_on_fail(
            dotenv.set_key(self.env_file, "TOP_K", str(config.TOP_K))
        )
        ok &= self.log_on_fail(
            dotenv.set_key(self.env_file, "FIRST_WORDS", str(config.FIRST_WORDS))
        )

        return ok

