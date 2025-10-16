import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

# Function to fetch jobs from Naukri (Web scraping example)
def fetch_naukri_jobs():
    url = "https://www.naukri.com/devops-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    job_list = []
    
    # Extract job data (adjust according to the actual Naukri page structure)
    for job in soup.find_all('article'):
        title = job.find('a', {'class': 'title'}).text.strip()
        job_url = job.find('a', {'class': 'title'})['href']
        posted_date = job.find('span', {'class': 'posted-date'}).text.strip()
        
        # Convert posted date to datetime format
        posted_datetime = datetime.strptime(posted_date, "%d %b %Y")
        
        # Filter jobs based on posting time (Last 24 hours or 3 days)
        if datetime.now() - posted_datetime <= timedelta(days=3):  # For last 3 days
            job_list.append({"title": title, "url": job_url, "posted_date": posted_datetime})

    return job_list

# Function to send email
def send_email(subject, body, to_email):
    from_email = "your-email@gmail.com"
    password = "your-email-password"  # Use app-specific password for Gmail

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    
    # SMTP server setup (Gmail in this case)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

# Main function to get job listings
def get_and_send_jobs():
    jobs = fetch_naukri_jobs()  # You can add other portals' functions here
    
    if jobs:
        # Format job listings to send in the email body
        email_body = "Here are the latest DevOps/SRE jobs:\n\n"
        for job in jobs:
            email_body += f"Job Title: {job['title']}\nPosted On: {job['posted_date']}\nLink: {job['url']}\n\n"
        
        send_email("Latest DevOps/SRE Jobs", email_body, "your-email@example.com")
    else:
        print("No jobs found.")

if __name__ == "__main__":
    get_and_send_jobs()
