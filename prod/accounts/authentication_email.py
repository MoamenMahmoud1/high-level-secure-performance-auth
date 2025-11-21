import logging
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__) 

class EmailAuthBackend:
    
    def authenticate(self, request ,username=None, password=None):
        logger.info(f"Trying to authenticate user/email: {username}")
        if not username or not password:
            logger.warning("Username or password not provided")
            return None

        try:
            user = User.objects.get(email=username)
            logger.info(f"Found user: {user.email}")
            if user.check_password(password):
                logger.info("Password correct, authentication successful")
                return user
            else:
                logger.warning("Password incorrect")
                return None
        except User.DoesNotExist:
            logger.warning(f"No user found with email: {username}")
            return None
        except User.MultipleObjectsReturned:
            logger.error(f"Multiple users found with email: {username}")
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            logger.warning(f"No user found with id: {user_id}")
            return None