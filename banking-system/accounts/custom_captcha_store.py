from captcha.models import CaptchaStore as BaseCaptchaStore

class CustomCaptchaStore(BaseCaptchaStore):
    class Meta:
        proxy = True
        app_label = 'accounts'  
