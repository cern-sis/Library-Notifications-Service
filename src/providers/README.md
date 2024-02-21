# Upgrading the Library Notifications Service through web scraping

This is an additional module to the existing Library Notifications Service (LNS), involving scraping publishers' websites to acquire information
on new releases. This currently works for Cambridge University Press, Springer, and Taylor & Francis. Unfortunately, 
since beginning the project, we have been disallowed to scrape the websites of Oxford
University Press and World Scientific.

#### Modules required
-beautifulsoup4\
-selenium

#### Running the code

To run the main cli, simply execute the file located at /Library-Notifications-Service/src/providers/cli.py. 
This will allow you to choose a publisher, subject, and directory where you want the file containing latest releases to be downloaded.
