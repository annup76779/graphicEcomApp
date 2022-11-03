## Project
```
This is the new project requirements;
Project Example Idea 
Build a site to sell your graphic design services(E-commerce Applications)

Main Technologies;
-HTML,CSS, JavaScript, Python +Django 
-Relational database(recommending MySQL or Postgres)
-Stripe payments 

External user’s goal:

Users can purchase graphical designs to address their needs.
Site owner's goal:

Earn money for doing freelance design work
Potential features to include:

Showcase prior work for clients based on different kinds of requests and the customer's testimonials.
Allow users to order a particular graphic to suit their goals. The user would fill out a form describing their needs, including fields such as type (e.g. icon, logo, poster), size and description, get an automatic quote and then pay. You may want to include a javascript calculator to display a preview of the quote, but make sure that the final price is determined on the server and cannot be manipulated directly by the user. Order notifications. Type of payments; Either single payment. This kind of payment system(B2C) often suits businesses that sell products, or one-time services. The other most common way to pay is a subscription(B2B).
where the customer pays a monthly or annual fee to access the services in a web application, This type of payment system suits businesses that sell services. In these cases it makes sense to charge a monthly fee for access.
The site owner, logging in as a particular user, would be able to see a list of all orders and then upload their completed work which would be made available to the customer.
Employ SEO, Social Media and Email strategies to market your product
Employ marketing strategies to increase brand reach
```

## Done yet!
1. `mainApp` is the main application.
2. Image Upload model in done, Model name is `Graphics`
3. Templates are not yet completed
4. `MySQL` database is used for database.
5. a `config.json` file is provided, populate the file for the connection to database.
6. install all the requirements from `requirements.txt` by command line using the command - `pip install -r requirements.txt`

### how to connect to database.
1. download the mysql server from [Download link for windows](https://cdn.mysql.com//Downloads/MySQLInstaller/mysql-installer-community-8.0.30.0.msi).
2. OR you can use any online service or domain service provider database facilities to connect to database.

### Run following commands to start running app
```
pip install -r requirements.txt
cd ecomApp
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### in case do some change in model then run following command 
```
python manage.py makemigrations
python manage.py migrate
```