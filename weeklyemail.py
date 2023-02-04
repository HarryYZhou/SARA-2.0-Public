import pandas as pd
from student_data import students
from portfolio_graph_alltime import latest_portfolio_value, percentage_change, percentage_change_orientation
from functions import send_email, create_email, attach_file_to_email
from logger import Logger


# Test
trial_test = True

# Prepare Logger
log = Logger('Weekly')
log.begin()

email_sender = "sarasiifbot2.0@gmail.com"
with open('./data/passwords.txt') as fp:
    email_password = fp.read()

# Tester
if trial_test:
    # If trial_test is true, set students to only contain my information for testing
    students = {'example@example.edu.au': {'Name': 'Example', 'Stocks': 'all', 'Sensitivity': 2}}

# Send the date in the subject so it can be tracked
date_str = pd.Timestamp.today().strftime('%d-%m-%Y')

email_subject = f"SIIF - Weekly Report ({date_str})"

try:
    for student in students:
        # Extract all student data from CSV
        student_name = students[student]['Name']
        html_email = f'''
        <html>
            <body>
                <p>Dear {student_name},<p>
                <p>Here's an update on the SIIF portfolio:<p>
                <p>The current portfolio value is ${latest_portfolio_value:.2f}, that is {percentage_change:.1f}% {percentage_change_orientation} from last week!<p>
                <img src='cid:image1' style='max-width:100%' width="600">
                <p>The above graph compares SIIF's current portfolio against several other strategies. They are:<p>
                <p>Investing entirely into the NASDAQ 100, or the ASX 200.<p>
                <p>Here is a breakdown of SIIF's current portfolio!<p>
                <img src='cid:image2' style='max-width:100%' width="600">
                <p>Have a fantastic day!<p>
                <p>From Sara 2.0 (SIIF Automated Reporting Assistant 2.0)<p>
                <img src='cid:image3' style='max-width:100%' width="300">
                <small><p>-------------------------------------------------------<p>
                <p>Code not available to the public just yet<p>
                <p>Disclaimer: This email is automated and the data/visualisations/calculations are subject to errors!<p>
                <p>This has not been checked by a human, please do not solely use it to inform your financial decisions.<p>
                </small>
            </body>
        </html>
        '''
        try:
            # Create an Email object
            weekly_email = create_email(email_sender, student, email_subject, html_email)
            attach_file_to_email(weekly_email, "./images/portfolio_graph.jpeg", {'Content-ID': '<image1>'})
            attach_file_to_email(weekly_email, "./images/share_graph.jpeg", {'Content-ID': '<image2>'})
            attach_file_to_email(weekly_email, "./images/SIIF Logo.png", {'Content-ID': '<image3>'})
            send_email(email_sender, student, weekly_email, email_password)
            # If the email is sent, log a success, otherwise, log a fail
            log.success(student_name)
        except:
            log.failure(student_name)
# Any errors will be logged
except:
    log.error(name='Error')
# No matter what, end emailing
finally:
    log.end()