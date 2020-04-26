from os import urandom
from unittest import TestCase
from unittest.mock import patch

from project.utils import xmail


class Test(TestCase):
    @patch.object(xmail, xmail.send_mail.__name__)
    def test_(self, mock_send_mail):
        placeholder = urandom(4).hex()
        email_to = f"email_{placeholder}@test.com"
        subject = f"subject_{placeholder}"
        mail_template_name = "invitation"
        context = {"link": placeholder}

        xmail.send_email(
            email_to=email_to,
            subject=subject,
            mail_template_name=mail_template_name,
            context=context,
        )

        mock_send_mail.assert_called_once()
