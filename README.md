# Carsa_Auto_Register

### To Use:
1. Clone Repository: \
	```$ git clone <url>```

2. Install chromedriver ([guide][1])
3. Install dependencies: \
	```$ pip3 install -r requirements.txt```
3. Change details in "Input Details" section to your own   (lines 36 - 43)
	```
	def main():
    	# Input Details START
    	netlinkid = "example_netlinkid"
    	password = "example_password"
    	day_r = "Wednesday"
    	date_r = "dd-mm-yyyy"
    	time_r = "5:00 PM - 6:45 PM"
    	headless = True    # Switch to False to see the bot work
    	# Input Details END
	```
4. Run it! \
	```$ ./register.py```
	
PS: Once slot is successfully booked, carsa will send you a confirmation email.

[1]: https://www.youtube.com/watch?v=dz59GsdvUF8
