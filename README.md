# vmcatsdogs
# Cats &amp; Dogs  

This is a simple web applications that allows users to vote for their preferred animal and displays the result.  

Few things you should know about the application:   
* The docker container running the application will expose the web UI on port 80.  
* * The application exposes a health endpoint at the address `/health` returning HTTP code 200 and the text `OK` in case of good health.  
* * The application uses a database file inside the container to store the results. The database file is located by default inside `/var/lib/cats-dogs/database`.  
* * The application will fail after a random time of 2 to 15 minutes.
