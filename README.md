# PlanIt
#### Video Demo:  <URL HERE>
#### Description: PlanIt is a web app created with Flask that allows users to create and use tables for budgeting, prayer lists, and birthday lists.

## Introduction
------------------------

PlanIt is a web application designed specifically for teens and young adults who want to organize their lives. Currently, PlanIt has three separate mini-apps: 
A Prayer List, a Budget, and a Birthday Tracker. PlanIt was created to provide a simple web application that would allow individuals to have access to many different
planning tools that all have the same landing page. This project provided challenges in creating SQL tables that provided proper details for each of the applications
without overlapping from one table to another. A second challenge was found in the creation of the initial Budget and Profile pages.


## Requirements
-----------------------

This web application requires nothing other than a computer browser.


## Installation
-----------------------

This web application does not require any installations.


## Configuration
----------------------

No configuration is required for this web application.


## Usage
----------------

This web application is very simple for users to navigate. The user must first register for an account if they do not already have one. Once, registered, they can
enter their login information, and are redirected to the homepage. On the homepage, the user can select from the three apps as to which they want to use. This web 
application uses sessions to store the browser's 'cookies', and to keep information privatized. There is also a logout button and a profile page, where the user 
can create and update their profile.


## Design
-----------------------

At the beginning of PlanIt's creation, the design was simply black-and-white. However, further through the process, I decided on a palatte of subtle pastel
coloring for the app. Each page on the site went through many different stages of design plans as well, to find the most efficient and aesthetically-pleasing combination.

## Files
-----------------------

### application.py
The basic framework of this web application was inspired by CS50's Finance project. I used the imports provided by it as a starting place for the structure
of this file. From there, each route was developed. This code was written using basic python syntax, and using functions from the helpers file. I decided to use
Flask for this project instead of using the combination of JavaScript, HTML, and CSS as I felt that using Flask (mainly Python) allowed for smoother code to be 
written. This also helped me achieve the design and plan for the web app that I envisioned.

### helpers.py
These functions were mainly inspired by CS50's Finance project. I used a similar structure to create an apology / error message landing page, and imported the
usd function for the budget app.

### project.db
project.db is the SQLite3 database used to keep track of all of the users and their specific information for the general web app and each specific app. Private
information such as passwords are encrypted with a hash function.


## Folders
---------------------------

### static
The static folder holds all of the images and the CSS stylesheet for this project.

### templates
The templates folder consists of each individual HTML page, along with a layout page that each additional page extends.

