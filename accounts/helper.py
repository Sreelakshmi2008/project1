import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


from dotenv import load_dotenv

load_dotenv()
client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])


# sendin otp to phone using twilio service
def send(phone):
    verify.verifications.create(to=phone, channel='sms')


# verifying code sent and code given by user
def check(phone, code):
    try:
        result = verify.verification_checks.create(to=phone, code=code)
    except TwilioRestException:
        return False
    return result.status == 'approved'