import logging
from rest_framework_simplejwt.tokens import RefreshToken
from jose import jwe
from django.conf import settings

logger = logging.getLogger(__name__)


priv_hex = settings.JWE_KEY


try:
    #hex string
    priv_bytes = bytes.fromhex(priv_hex)
except ValueError:

    priv_bytes = priv_hex.encode()

#logger.debug(f"Using JWE key bytes: {priv_bytes.hex()}")

# Seetings JWE
JWE_ALG = "A256KW"
JWE_ENC = "A256CBC-HS512"


class EncryptedRefreshToken(RefreshToken):
    def encrypt(self):
        """
        Return Refrsh token Encrypted
        """
        signed_token = str(self)
        try:
            encrypted = jwe.encrypt(
                signed_token.encode(),
                priv_bytes,
                algorithm=JWE_ALG,
                encryption=JWE_ENC
            )
            return encrypted.decode()
        except Exception as e:
            logger.error(f"Error encrypting refresh token: {e}")
            raise

    @staticmethod
    def decrypt(encrypted_token):
        """
        decrypred token
        """
        try:
            decrypted = jwe.decrypt(
                encrypted_token,
                priv_bytes
            ).decode()
            return decrypted
        except Exception as e:
            logger.error(f"Error decrypting refresh token: {e}")
            return None
