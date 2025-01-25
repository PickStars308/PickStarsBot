from typing import Optional


from nonebot import get_plugin_config
from pydantic import BaseModel, Field

class Config(BaseModel):
    administrator: Optional[int] = Field(default=None)


plugin_config: Config = get_plugin_config(Config)
Administrator = plugin_config.administrator