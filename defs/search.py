import email.header
from datetime import date, datetime, timedelta
from typing import List

from cashews import cache
from imapclient import IMAPClient

from defs.models import Mail
from glover import host, days, username, password


def decode_mime_words(s):
    return u''.join(
        word.decode(encoding or 'utf8') if isinstance(word, bytes) else word
        for word, encoding in email.header.decode_header(s))


def get_date() -> date:
    now = datetime.now()
    old = now - timedelta(days=days)
    return date(old.year, old.month, old.day)


async def filter_mail(ids: List[int]) -> List[int]:
    new = []
    for mid in ids:
        if await cache.get(f"mail:{username}:{mid}"):
            continue
        new.append(mid)
    return new


async def search() -> List[Mail]:
    with IMAPClient(host=host) as client:
        client.login(username, password)
        client.select_folder("INBOX")

        messages = client.search([u'SINCE', get_date()])
        messages = await filter_mail(messages)
        response = client.fetch(messages, ["RFC822"])
        mails = []
        for message_id, data in response.items():
            email_message = email.message_from_bytes(data[b"RFC822"])
            from_ = email_message.get("From")
            subject = decode_mime_words(email_message.get("Subject"))
            to = email_message.get("To")
            mail = Mail(
                id=message_id,
                from_=from_,
                subject=subject,
                to=to,
            )
            mails.append(mail)
        return mails
