from django.contrib.auth.tokens import PasswordResetTokenGenerator
import logging

logger = logging.getLogger(__name__)

class BaseTokenGenerator(PasswordResetTokenGenerator):
    """
    Generate tokens depends on fields
    """
    fields = []

    @classmethod
    def set_fields(cls, *fields):
        cls.fields = list(fields)
        logger.info(f"{cls.__name__} fields set to: {cls.fields}")

    def _make_hash_value(self, user, timestamp):
        if self.fields:
            values = ''.join(str(getattr(user, f, '')) for f in self.fields)
        else:
            values = str(user.pk) + str(user.is_active)

        hash_value = str(timestamp) + values
        logger.debug(f"{self.__class__.__name__} hash for user {user.username}: {hash_value}")
        return hash_value


# for activation email
activation_token_generator = BaseTokenGenerator()
activation_token_generator.set_fields("is_active", "is_verified")

#for password reset
password_reset_token = BaseTokenGenerator()
password_reset_token.set_fields("password_time_edited", "username")
