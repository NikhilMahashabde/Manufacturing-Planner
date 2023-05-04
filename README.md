

# Project 2 manufac alpha static site

Purpose - just build a really solid app that does everything, is
secure, 
fast,
efficient 

and allows me to learn things
JWT
Bootstrap extended. 
OOP - class and service setup

**routes**

[
/workorders/api
/workorders/api/<id>

]

/forms/users/update
- update all user data and passwords - admin only. 04/05

**features**
** work order page **

- main WO page to show all WOs
- edit WO -> take you to WO specific page
- add flags to WOs


**LOGIN AND SECURITY **
- login with session token
- registration page for new users (this really shouldnt exist, this is not an app made for public, but has been included for sake of project)
- [tba] - account password reset. 
- administrator page
  - create new user (similair to new user registration but can set up as admin user)
  - delete existing user
  - update all user info as per table
    - change password is here

- secure routing for public, private, and admin 

[styling]
bootstrap has been used yet again
- update UIs for registration
- log in UI
- main work order page UI
- 



**wish list - TBA**

split app into micro service architecture - main app is just for security service
pull in work order data from external APi 

    - login with session token
    - if logged in, send back jwt
    - send back site to private home page route
    - site includes js 
    - js to call json data with jwt header

    - site will check jwt token against main site to authenticate token 

pull in requsitions from external API




# README

This is the [Flask](http://flask.pocoo.org/) [quick start](http://flask.pocoo.org/docs/1.0/quickstart/#a-minimal-application) example for [Render](https://render.com).

The app in this repo is deployed at [https://flask.onrender.com](https://flask.onrender.com).

## Deployment

Follow the guide at https://render.com/docs/deploy-flask.
