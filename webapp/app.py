from bokeh.plotting import figure
from bokeh.embed import components
from flask import Flask, render_template
from collections import Counter
import requests
import datetime

app = Flask(__name__)

@app.route("/")
def chart():
    r = requests.get('http://auth.chargeup.asia:1337/user')
    data = r.json()
    current_date = datetime.datetime.now().date()
    prev_date = current_date + datetime.timedelta(-100)
    
    no_of_users = len(data)
    
    virtual = 0
    for user in data:
        if "virtual" in user:
            virtual += 1
    non_virtual = no_of_users - virtual
    
    updated_stamps = []
    stamp_users = []
    stamp_dates = []
    for user in data:
        if "updatedAt" in user:
            updated_stamps.append(user['updatedAt'].split('T', 1)[0])

    stamps_tally = Counter(updated_stamps).most_common(10)

    for date in stamps_tally:
        stamp_users.append(date[1])
        stamp_dates.append(date[0])
        
        
    email_data = []
    email_counter = []
    email_tally = []
    
    email_users = []
    email_types = []
    for user in data:
        if "email" in user:
            email_data = (user['email'].split('@', 1))
            #some of the email data only contained the username
            if len(email_data)>1:
                email_tally.append(email_data[1])
                
    email_counter = Counter(email_tally).most_common()
    for email in email_counter:
        email_types.append(email[0])
        email_users.append(email[1])
        
    
    p1 = figure(plot_width = 600, plot_height = 600, title = 'Virtual and non-virtual', x_axis_label = 'virtual/non-virtual', y_axis_label = 'number of users')
    p1.vbar(x= [1,2], top = [virtual, non_virtual], width = 0.9, fill_color = "#6599ed")
    p2 = figure(x_axis_type = "datetime", plot_width = 600, plot_height = 600, title = "Last updated stamps", x_axis_label = 'timestamps', y_axis_label = 'users')
    p2.line(x = stamp_dates, y = stamp_users, line_width =2)
    p3 = figure(y_range = email_types, plot_width = 600, plot_height = 600, title = 'Types of email')
    p3.hbar(y = email_types, right = email_users, height = 0.9, fill_color = '#6599ed')
    
    plots = [p1, p2, p3]
    script, div = components(plots)
    
    return render_template("chart.html", the_div = div, the_script = script)
    
if __name__ == "__main__":
    app.run(debug = True)
    
