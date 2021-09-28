"""Util code for sending and handling emails"""
from __future__ import annotations
from typing import List, Union, Dict, Tuple
import logging

from django.conf import settings

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Asm, GroupId, Mail
from sendgrid.helpers.mail.exceptions import SendGridException

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
logger.setLevel(logging.INFO)


def send_template_email(
    from_email: Union[str, Tuple[str]],
    to_emails: Union[str, List[str]],
    template_id: str,
    template_data: Dict[str, str],
    attachment=None,
):
    """Sends an email with template and data to specified addresses"""
    message = Mail(from_email=from_email, to_emails=to_emails)

    asm = Asm(GroupId(int(settings.SENDGRID_GROUP_ID)))
    message.asm = asm
    message.template_id = template_id
    message.dynamic_template_data = template_data

    if attachment is not None:
        message.attachment = attachment
    try:
        sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        msg = sendgrid_client.send(message)
        logger.debug(
            "Successfully sent email with template %s to address %s",
            template_id,
            str(to_emails),
        )
        return msg
    except SendGridException as error:
        logger.error(
            "Failed to send email with template %s to address %s with error: %s",
            template_id,
            str(to_emails),
            str(error),
            exc_info=True,
        )
        raise error
