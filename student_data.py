import pandas as pd
student_data = pd.read_csv('./data/student_data.csv')

students = {}

for name, email, stocks, sensitivity in student_data[['Name', 'Email', 'Stocks', 'Sensitivity']].values:
    students[email] = {'Name': name, 'Stocks': stocks, 'Sensitivity': sensitivity}