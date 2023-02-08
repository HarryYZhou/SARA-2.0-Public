import pandas as pd
from student_data import students
from dailystocktracker import share_return_dict
from functions import send_email, create_email, attach_file_to_email
from logger import Logger
import datetime as dt
today = dt.datetime.utcnow()
# Convert UTC time of PythonAnywhere to Melbourne time (11 hours)
ten_hours_from_utc = today + dt.timedelta(hours=11)
weekday = ten_hours_from_utc.weekday()

# Check if monday-friday
if weekday in [0, 1, 2, 3, 4]:

    # Test
    trial_test = True

    # Prepare Logger
    log = Logger('DAILY')
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

    email_subject = f"SIIF - Daily Report ({date_str})"

    try:
        for student in students:
            # Extract all student data from CSV
            student_name = students[student]['Name']
            student_sensitivity = students[student]['Sensitivity']
            share_return_to_send = {}
            shares_to_research = []
            html_email = f'''
            <html>
                <body>
                    <p>Dear {student_name},<p>'''
            # Check if the share change is larger than sensitivity for each share
            for share in share_return_dict:
                if abs(share_return_dict[share]) > abs(student_sensitivity):
                    share_return_to_send[share] = share_return_dict[share]
                    shares_to_research.append(share)
            # If it is larger, add to separate dict

            # If there are no shares with increased sensitivity, move on to next student
            if share_return_to_send == {}:
                log.passed(student_name)
                continue

            if share_return_to_send:
                for share, value in share_return_to_send.items():
                # Add these shares to the email
                    if value <= -2:
                        value *= -1 * student_sensitivity
                        html_email += f'''
                    <p>Today {share} dropped {value:.1f}%<p>'''
                    elif value >= -1 * student_sensitivity:
                        html_email += f'''
                    <p>Today {share} rose {value:.1f}%<p>'''
                first_share_to_research = shares_to_research[0]
                html_email += f"""
                    <p>You may like to investigate why, click <a href="https://www.google.com.au/search?q={first_share_to_research}+asx">here</a> to begin your research!<p>"""
            # TODO Setup GITHUB and share code
            html_email += f'''
                    <img src='cid:image1' style='max-width:100%' width="600">
                    <p>Have a fantastic day!<p>
                    <p>From Sara 2.0 (SIIF Automated Reporting Assistant 2.0)<p>
                    <img src='cid:image2' style='max-width:100%' width="300">
                    <small><p>-------------------------------------------------------<p>
                    <p>Code available at https://github.com/HarryYZhou/SARA-2.0-Public<p>
                    <p>Disclaimer: This email is automated and the data/visualisations/calculations are subject to errors!<p>
                    <p>This has not been checked by a human, please do not solely use it to inform your financial decisions.<p>
                    </small>
                </body>
            </html>
            '''
            try:
                # Create an Email object
                daily_email = create_email(email_sender, student, email_subject, html_email)
                attach_file_to_email(daily_email, "./images/weekly_graph.jpeg", {'Content-ID': '<image1>'})
                attach_file_to_email(daily_email, "./images/SIIF Logo.png", {'Content-ID': '<image2>'})
                send_email(email_sender, student, daily_email, email_password)
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