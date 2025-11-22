from jose import jwe
from django.conf import settings
from django.urls import resolve
import logging
logger = logging.getLogger(__name__)
priv = settings.JWE_KEY
JWE_ALG = "A256KW"
JWE_ENC = "A256CBC-HS512"



class DecryptRefreshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        try:
            resolve_match = resolve(request.path).url_name
        except Exception:
            
            return self.get_response(request)
        try:
            priv_hex = bytes.fromhex(priv)

        except Exception as e:
            logger.debug(f"error is: {e}")
            priv_hex = priv.encode()

        
        request.refresh_token_decrypted = None
        

        try:
            resolve_match = resolve(request.path).url_name
            logger.debug(f"Url name: {resolve_match}")

            if resolve_match.endswith("_refresh_token"):
                logger.debug("Inside refresh token resolve")

                uid = request.headers.get("X-Active-User")  # أو request.META.get("HTTP_X_ACTIVE_USER")
                logger.debug(f"user id {uid}")
                if uid:
                    encrypted = request.COOKIES.get(f"refresh_token_{uid}")
                    logger.debug(f"Encrypted refresh_token: {encrypted}")

                    if encrypted:
                        try:
                            decrypted = jwe.decrypt(encrypted.encode(), priv_hex).decode()
                            request.refresh_token_decrypted = decrypted
                            logger.debug(f"Decrypted refresh token set ✅")
                        except Exception as e:
                            logger.debug("JWE decryption error: %s", e)
            else:
                logger.debug("NOt in used this middleware   ")

        except Exception as e:
            logger.debug("DecryptRefreshMiddleware error: %s", e)

        response = self.get_response(request)
        return response
