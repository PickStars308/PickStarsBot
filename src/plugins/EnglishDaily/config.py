from typing import Optional

from nonebot import get_plugin_config
from pydantic import BaseModel, Field


class Config(BaseModel):
    toutiaoapi: Optional[str] = Field(default=None)


plugin_config: Config = get_plugin_config(Config)
TOUTIAOAPI = plugin_config.toutiaoapi