import datetime



while 1:
    date = datetime.datetime.now()
    if date.day == day_to_run and date.month == month_to_run:
        break # this breaks out of the while loop if it's the right day.
    else:
        sleep(60) #wait 60 seconds

# schedule.every(60).minutes.do(job) #continue with the rest of the program
# schedule.every().hour.do(job)
# schedule.every().day.at("18:36").do(job)

while 1:
    schedule.run_pending()
    sleep(1)