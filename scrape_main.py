import os
from time import sleep
from datetime import datetime, timedelta
from scrape_aljazeera import scrape_aljazeera
from scrape_cnn import scrape_cnn
from scrape_jpost import scrape_jpost


os.environ['OPENAI_API_KEY'] = 'YOUR_API_KEY'

# Define start and end dates
start_date = datetime.strptime('10-28-2023', '%m-%d-%Y')
end_date = datetime.strptime('11-30-2023', '%m-%d-%Y')

# Iterate over date range
current_date = start_date
while current_date <= end_date:
    # Format the date as a string if needed, e.g., '10-27-2023'
    date_str = current_date.strftime('%m-%d-%y')
    print(date_str)
    
    # Call scraping functions with the formatted date string
    try:
        scrape_jpost(date_str)
    except Exception as e:
        print(f"Error Scraping Jerusalem Post on {date_str}: \n {e}")
    
    try:
        scrape_cnn(date_str)
    except Exception as e:
        print(f"Error Scraping CNN on {date_str}: \n {e}")
        
    try:
        scrape_aljazeera(date_str)
    except Exception as e:
        print(f"Error Scraping Al Jazeera on {date_str}: \n {e}")
    
    # Increment the date by one day
    current_date += timedelta(days=1)
    sleep(1)
    

