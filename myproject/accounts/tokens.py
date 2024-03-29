from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

#using TokenGenerator class we can create a unique token for confirmation
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()