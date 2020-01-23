from smtplib import SMTPException
from unittest import mock

from pytest import mark

from django.contrib.auth import get_user_model

from .testCases import RelayTestCase, DefaultTestCase
from graphql_auth.constants import Messages
from graphql_auth.utils import get_token, get_token_paylod


class RegisterTestCaseMixin:
    def test_register_invalid_password_validation(self):
        """
        fail to register same user with bad password
        """

        # register
        executed = self.make_request(self.register_query("123"))
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"])

    def test_register(self):
        """
        Register user, fail to register same user again
        """

        # register
        executed = self.make_request(self.register_query())
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)

        # try to register again
        executed = self.make_request(self.register_query())
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"]["username"])

    @mock.patch(
        "graphql_auth.models.UserStatus.send_activation_email",
        mock.MagicMock(side_effect=SMTPException),
    )
    def test_register_email_send_fail(self):
        executed = self.make_request(self.register_query())
        self.assertEqual(executed["success"], False)
        self.assertEqual(
            executed["errors"]["nonFieldErrors"], Messages.EMAIL_FAIL
        )
        self.assertEqual(len(get_user_model().objects.all()), 0)

    @mark.settings_b
    def test_register_with_dict_on_settings(self):
        """
        Register user, fail to register same user again
        """

        # register
        executed = self.make_request(self.register_query())
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)

        # try to register again
        executed = self.make_request(self.register_query())
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"]["username"])


class RegisterTestCase(RegisterTestCaseMixin, DefaultTestCase):
    def register_query(self, password="akssdgfbwkc"):
        return """
        mutation {
            register(
                email: "test@email.com",
                username: "username",
                password1: "%s",
                password2: "%s"
            )
            { success, errors  }
        }
        """ % (
            password,
            password,
        )

    def verify_query(self, token):
        return """
        mutation {
            verifyAccount(token: "%s")
                { success, errors }
            }
        """ % (
            token
        )


class RegisterRelayTestCase(RegisterTestCaseMixin, RelayTestCase):
    def register_query(self, password="akssdgfbwkc"):
        return """
        mutation {
         register(
         input:
            { email: "test@email.com", username: "username", password1: "%s", password2: "%s" }
            )
            { success, errors  }
        }
        """ % (
            password,
            password,
        )

    def verify_query(self, token):
        return """
        mutation {
        verifyAccount(input:{ token: "%s"})
            { success, errors  }
        }
        """ % (
            token
        )
