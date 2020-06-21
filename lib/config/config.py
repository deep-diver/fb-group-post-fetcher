from __future__ import annotations


class Config:
    FB_GROUP_ID: str
    FB_ACCESS_TOKEN: str

    FB_APP_ID: str
    FB_APP_SECRET: str

    SMTP_USER: str
    SMTP_PASS: str

    TOP_K: int
    FIRST_WORDS: int

    @classmethod
    def of(cls, **kwargs) -> Config:
        c = cls()
        c.FB_GROUP_ID = kwargs.get("FB_GROUP_ID")
        c.FB_ACCESS_TOKEN = kwargs.get("FB_ACCESS_TOKEN")
        c.FB_APP_ID = kwargs.get("FB_APP_ID")
        c.FB_APP_SECRET = kwargs.get("FB_APP_SECRET")
        c.SMTP_USER = kwargs.get("SMTP_USER")
        c.SMTP_PASS = kwargs.get("SMTP_PASS")

        c.TOP_K = int(kwargs.get("TOP_K", "10"))
        c.FIRST_WORDS = int(kwargs.get("TOP_K", "10"))
        return c

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Config):
            return False

        return (
            self.FB_GROUP_ID == o.FB_GROUP_ID
            and self.FB_ACCESS_TOKEN == o.FB_ACCESS_TOKEN
            and self.FB_APP_ID == o.FB_APP_ID
            and self.FB_APP_SECRET == o.FB_APP_SECRET
            and self.SMTP_USER == o.SMTP_USER
            and self.SMTP_PASS == o.SMTP_PASS
            and self.TOP_K == o.TOP_K
            and self.FIRST_WORDS == o.FIRST_WORDS
        )

    def __repr__(self) -> str:
        return f"""Config(
    FB_GROUP_ID: {self.FB_GROUP_ID}
    FB_ACCESS_TOKEN: {self.FB_ACCESS_TOKEN}
    FB_APP_ID: {self.FB_APP_ID}
    FB_APP_SECRET: {self.FB_APP_SECRET}
    SMTP_USER: {self.SMTP_USER}
    SMTP_PASS: {self.SMTP_PASS}
    TOP_K: {self.TOP_K}
    FIRST_WORDS: {self.FIRST_WORDS}
)"""

