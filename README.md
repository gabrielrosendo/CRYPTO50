# CS50 Final Project - CRYPTO50

![Blue Doodle Mind Map Timeline Brainstorm](https://github.com/gabrielrosendo/CRYPTO50/assets/71938938/2843786d-e95b-4a37-b772-74f292992722)


#### Video Demo:  <https://www.youtube.com/watch?v=5bgLvp2HXPk>
### Completed in September/2021
#### Description:
CRYPTO50 is a web application developed as the final project for CS50. It allows users to simulate investing in cryptocurrencies without actually having to spend any money. Users can create or login to an account, and they will start with $10,000 to buy different cryptocurrencies.

Technologies used:

- Python
- Flask
- HTML
- CSS
- JQUERY

## How does the webpage work?

To begin using, the user must create or login to an account. In this account, every user will start with $10.000, and they can use this money to buy different cryptocurrencies and
simulate investing in cryptocurrencies without actually having to spend any money. In the homepage the website provides to the user all tha latest information about the cryptos they currently have,
such as the current value and the change in the last 24 hours. Besides that, the homepage also shows boxes with all the latest important news and articles about cryptocurrencies, by clicking on the box,
the user is taken to a link in which they can read the article. The user can also sell their cryptos and read more about by going to the "Understand Crypto" page.

### Database

Database stores all users, hashed passwords, cash the users have, what cryptocurrencies the user has and information about every one of them.

### Sessions

The webpage uses sessions to confirm that user is registered. Once the user tries to logins, his password is hashed and checked. Once everything passes a session is created and stored.
The server attaches user to subsequent requests, so the back-end can easily access the details in the database for each user.

## Files

Static and templates files contain the CSS and HTML code, respectively. I used some bootstrap for the stylying and followed some tutorials online. 
Application.py contain the python code for the application and apy.py contains someextra functions that are used in application.py. 
These functions are the ones that read the API information and output the desired information. 
Crypto.db contains the database, which is divided in users, containing info about the user, and portfolio, that contains info about which users hold which cryptocurrencies and also a lot of information about the cryptocurrencies.

## How to launch application

To run the web application use this command on the terminal:

$ flask run

## Possible improvements

As all applications this one can also be improved. Possible improvements that I might add once I get more fammiliar with programming:

- Add the possibility to add and withdraw cash.
- Ability to change account details
- Homepage shows graphic of the most important crypto in the last 7 days.
- Have a way for users to send their suggestions and problems via chat.
- Register with email and notificaitons to email about new prices and essential information about account.
