from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyrogram import Client
    from pyrogram.types import Message

TEMP = """#mail 
✉️ %s (%s)
To: <code>%s</code>

%s"""


class Mail(BaseModel):
    id: int
    from_: str
    subject: str
    to: str

    @property
    def from_name(self) -> str:
        li = self.from_.split(" <")
        return " <".join(li[:-1]).strip()

    @property
    def from_at(self) -> str:
        li = self.from_.split(" <")
        return li[-1].strip()[:-1]

    @property
    def text(self) -> str:
        return TEMP % (self.from_name, self.from_at, self.to, self.subject)

    async def send(self, bot: "Client", chat_id: int) -> "Message":
        return await bot.send_message(chat_id, self.text)
