# microservices
An online store that uses several decoupled services to operate.

# Setup
## Dependency tree
database -> rest API -> web server, admin server

## Database Container
* Build container by running `docker-compose build`
* Start container by running `docker-compose up`

## Rest API Container
* Edit `rest-api/docker-compose.yml` to add the endpoint of the database container
* Build container by running `docker-compose build`
* Start Container by running `docker-compose up`

## Admin Server Container
* Edit `admin-server/docker-compose.yml` to add the endpoint of the rest-api container.
* Build container by running `docker-compose build`
* Start Container by running `docker-compose up`

## Web Server Container
* Edit `web-server/docker-compose.yml` to add the endpoint of the rest-api container
* Build container by running `docker-compose build`
* Start Container by running `docker-compose up`

# How It Works!
* Admins can add items to the store using their admin page.
* Users can add items to their cart, then order the items.
* Admins see an order to be fulfilled, goes ahead and fulfills it.

## Other features
* Users can see their order history.
* Both Users and Admins can change account information like first and last name, password.
* Admins can see fulfilled and unfulfilled orders.

# Demo
![Screenshot from 2019-08-10 17-14-49](https://user-images.githubusercontent.com/24194821/62877354-d69a7680-bcf4-11e9-9198-e17e7e286eee.png)
Login page of the Web Server running on AWS ECS

![Screenshot from 2019-08-10 17-15-16](https://user-images.githubusercontent.com/24194821/62877484-22e5b680-bcf5-11e9-9f45-f31812d578ca.png)
Sign Up page of the Web Server running on AWS ECS

