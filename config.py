from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Config:
    bot_token: str
    admin_id: int


def load_config() -> Config:
    token = getenv("BOT_TOKEN", "YOUR_BOT_TOKEN").strip()
    admin_raw = getenv("ADMIN_ID", "6936232244").strip()
    return Config(bot_token=token, admin_id=int(admin_raw))


config = load_config()
