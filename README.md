# bangkit_final_webapp
webapp repository of makeup detection model
the webapp is built using flask and hosted to heroku cloud platform. python script in flask app will call the api to our makeup model which is deployed on google AI-platform, then display the result of prediction of an image to the web browser.

link to our webapps: https://bangkit-demo.herokuapp.com/

To host the flask app as a heroku web application, we need to use Gunicorn WSGI. see the list of libraries dependencies in requirements.txt before pushing to heroku and include the Procfile.
