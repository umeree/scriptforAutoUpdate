


from urllib.request import urlopen
from html.parser import HTMLParser
import smtplib
import time

# Email credentials
# Email credentials
EMAIL_ADDRESS = 'umernadeam@gmail.com'
EMAIL_PASSWORD = 'Jinnah_4832'
TO_EMAIL = 'umernadeam@gmail.com'

# BLS Italy Pakistan website credentials
USERNAME = 'umernadeam@gmail.com'
PASSWORD = 'Jinnah_4832'

# URLs
LOGIN_URL = 'https://blsitalypakistan.com/account/login'
APPOINTMENT_URL = 'https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment'


# Check interval (in seconds)
CHECK_INTERVAL = 60  # 1 minute

# Function to send email notification
def send_email():
    subject = 'Appointment Available'
    body = 'Appointments are now available on the website. Visit ' + APPOINTMENT_URL + ' to book an appointment.'
    message = f'Subject: {subject}\n\n{body}'

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, message)
    print('Email sent')

# Custom HTML parser to check for appointment status
class AppointmentHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.available_dates = []

    def handle_starttag(self, tag, attrs):
        if tag == 'input' and ('id', 'valAppointmentDate') in attrs:
            for attr, value in attrs:
                if attr == 'value':
                    self.available_dates.append(value)

def check_appointments(selected_date):
    print('Checking appointments for:', selected_date)
    response = urlopen(APPOINTMENT_URL)
    html_content = response.read().decode('utf-8')
    
    parser = AppointmentHTMLParser()
    parser.feed(html_content)
    
    print('Available Dates:', parser.available_dates)
    
    if selected_date in parser.available_dates:
        send_email()
        return True
    return False

# Main loop to keep checking the website
def main():
    while True:
        # Example: Replace '2024-06-20' with the actual selected date from the calendar input
        if check_appointments('2024-06-20'):
            break
        print('No appointments available for the selected date. Waiting...')
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
