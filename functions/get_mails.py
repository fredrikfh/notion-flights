import datetime
import email
import imaplib
import os
import quopri
from contextlib import closing
from email.header import decode_header

from dateutil.parser import parse

from functions.console import log
from functions.get_html import get_data_from_html
from functions.mail_parsers.non_specific_dates import non_specific_dates
from functions.mail_parsers.specific_dates import specific_dates
from functions.parse_date import parse_date

TEXT_PLAIN = "text/plain"
SUBJECT_LINE = "Subject"
SPECIFIC_ROUTE = "ruten du sporer"


def get_mails(number: int):
    """
    This function connects to an email server, retrieves the last three emails, and parses their content.

    Args:
    number: int, the number of emails to fetch.

    Returns:
    parsed_data: list, contains parsed email data from the last three emails.
    """
    try:
        with closing(imaplib.IMAP4_SSL(os.getenv("EMAIL_IMAP"))) as mail:
            rv, data = mail.login(
                os.getenv("EMAIL_USERNAME"), os.getenv("EMAIL_PASSWORD"))
            if rv != 'OK':
                log("Unable to log in to email server", "danger")
                return None

            mail.select("INBOX")

            # Get the list of email IDs
            result, data = mail.uid('search', None, "ALL")
            email_ids = data[0].split()

            # Get the latest three email IDs
            latest_email_ids = email_ids[-number:]

            # Parse the emails
            parsed_data = []
            for email_id in reversed(latest_email_ids):
                result, email_data = mail.uid(
                    'fetch', email_id, '(BODY[TEXT])')
                raw_email = email_data[0][1].decode("utf-8")

                # Parse the raw email
                email_message = email.message_from_string(raw_email)

                subject = None
                # Get the email part and decode it
                for part in email_message.walk():
                    if part.get_content_type() == TEXT_PLAIN:  # ignore attachments/html
                        byte_code = part.get_payload(decode=True)
                        if byte_code:
                            decoded_bytes = quopri.decodestring(byte_code)
                            email_text_content = decoded_bytes.decode("utf-8")

                            # Extract HTML content from the string
                            start_html = email_text_content.find('<html')
                            end_html = email_text_content.rfind('</html>')
                            if start_html != -1 and end_html != -1:
                                html_content = email_text_content[start_html:end_html + 7]
                                html_data = get_data_from_html(
                                    html_content, "tr")

                                route = find_words_around_til(html_content)

                                if "Prisene er endret for følgende destinasjoner" in html_content:
                                    log("specific dates", "warning")
                                    parsed_data.append(
                                        specific_dates(html_data))
                                elif "Vi har funnet" in html_content:
                                    log("non-specific dates", "warning")
                                    parsed_data.append(
                                        non_specific_dates(html_data, route))
                                else:
                                    log("unknown email type", "danger")

            return parsed_data

    except imaplib.IMAP4.error as error:
        log(f"An error occurred: {error}", "danger")
        return None


def find_words_around_til(text):
    words = text.split()
    stop_words = ["class", "</div>", ".", "i januar", "i februar", "i mars", "i april", "i mai",
                  "i juni", "i juli", "i august", "i september", "i oktober", "i november", "i desember"]
    if 'til' in words:
        til_index = words.index('til')
        word_before = words[til_index - 1] if til_index > 0 else None
        words_after = []
        for word in words[til_index + 1:]:
            if any(stop_word in word for stop_word in stop_words):
                # Find the position of the stop word in the word
                stop_word_index = min(word.find(stop_word)
                                      for stop_word in stop_words if stop_word in word)
                words_after.append(word[:stop_word_index])
                break
            words_after.append(word)

        return (word_before + " til " + ' '.join(words_after)).split(" i ")[0]
    else:
        return None, None
