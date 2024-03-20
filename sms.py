# create a function to send sms upon registration
# github.com/modcomlearning/web step 12

# sending an sms
import africastalking
africastalking.initialize(
    username="joe2022",
    api_key="adfvyuh977efetgsgsgszdv"
    #justpaste.it/1nua8
)
sms = africastalking.SMS
def send_sms(phone, message):
    recipients = [phone]
    sender = "AFRICASTKNG"
    try:
        response = sms.send(message, recipients)
        print(response)
    except Exception as error:
        print("Error is ", error)
	