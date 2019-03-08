SocialReach..

"Note": The credentials used for the authentication, authorization and getting data from twitter has been removed from the authentication.py
file, if you want to run this app then you can easily put your own creadentials in authentication.py file and successfully run the whole code.

This project has been created by Muhammad Sameer Khan and Hasnain Ahmed Khan for the purposes of final year project and has been submitted as a final year project. The main code structure of this program
is as follows:

1)It has been created in Django(python) as a web application.

2)It contains three views which are basically the functions which contain back-end logic of program, the first view is named 'Index'
it is for the purpose to return the homePage of the application as the result of the very first request generated, the second view
is 'PostIndex' it is for the handling of POST request from the homepage which ccontains the username of the user which the application
user wants to mine, this view contains all the core logic of the application it uses the userName of the user and gathers all the data
from the manipulating functions and send it to the template(HTML) to show the data on the screen. The third view is 'TimeSeries' which
is for the purpose of creating time series of the user tweets and return the http response which contains an image string.

3)The project contains two templates i.e. HTML pages, one is named 'index' which is for the homePage purpose and other is 'PostIndex'
which is for the purpose of representing the data which we are getting from the PostIndex view.

4)There are two othe files or we can say modules which are created by us and the contain all the methods(functions) which we are using
in the program. one module is named 'authentication.py' which contains all the methods and logic to create a secure connection with
twiiter and other is 'methods.py' which contains all the methods which we are using in our PostIndex view for the manipulation of data
which we are getting from twitter.

5)No database is used in this project. The project has been designed in the way that all the gathering and manipulation of data has been
taking place in realtime.

This is a very breif summary of the project. I hope if you want to understand this project than this README file will help you.