# QrGeneratorapp

[![Build Status](https://github.com/capinho/Qrcodeapp/actions/workflows/django.yml/badge.svg)](https://github.com/capinho/Qrcodeapp/actions/workflows/django.yml)

[![Coverage Status](https://coveralls.io/repos/github/capinho/Qrcodeapp/badge.svg?branch=main)](https://coveralls.io/github/capinho/Qrcodeapp?branch=main)

## Project Catalogue

- [Project Scope](#project-scope)
- [Problem Statement](#problem-statement)
- [Research Background](#research-background)
  - [Modalities](#modalities)
  - [Niche](#niche)
- [Set Up and Installation](#set-up-and-installation)
- [Technologies Used](#technologies-used)




## Project Scope

           QR Code- Quick response Code
            
-It is basically a collection/array of barcodes with black and white squares that are mainly machine-readable codes.

-It can be used for storing URLs and other information.

-They are capable of storing lots of data/information that can be read by a digital device, eg cell phones

-It gives more information about a user to prospects.


## Problem Statement

QR codes are fast becoming popular these days. Most people are drifting away from the traditional mode of advertising/marketing and just storing their digital information online in QR codes. QR codes are everywhere we go now; banks, hospitals, hotels, restaurants etc. But the question on everyone’s lips is how do they come about these codes?

These codes are generated online by an online software called QR code generator. From secondary research, a lot of these platforms are not simplified enough for beginners to use. And to tackle that problem, we will be following the popular saying: “Less is more.” We will design a platform that allows users to generate QR codes with less hassle. The QR code generated can be downloaded, shared online amongst many other features and when scanned will lead to the user’s portfolio website or catalogue.


## Research Background


We aim to design and build a platform that allows users to generate QR code that leads to their portfolio website or catalogue when scanned. 
QR code generators are fast becoming popular these days. They allow people access digital information with a quick scan. The ‘QR’ in QR code means quick response. Any type of digital information can be stored in these codes. A QR generator is an online software that is used to create or generate these QR codes that store digital information. 
There are two types of QR codes; static and dynamic. The digital information in static QR codes cannot be edited once it is generated but in dynamic QR codes, the information can be edited even after the QR code is generated. 

### Modalities

#### User: Unauthenticated

-1st and 2nd features.

The first requirement is that users should visit the platform and get to see information about the platform. Hence, a landing page for the project. The second feature entails a view demo button.

-3rd and 4th features.

The 3rd feature includes a sign up page /login page and 4th feature suggests (as required) a functionality to the sign up fields (which means that anyone that visits the site will be required to login first, before getting to see all other features/functionalities of the site).


#### User: Authenticated

- Once the users login, they get full access to the platform.
- Generated QR codes can be downloaded, shared online amongst many other features and when scanned will lead to the users' portfolio websites or catalogues.
- User Dashboard Section Design - A personal space for the user to save and manage (manipulate) their respective QR codes.
- Allow user save data and come back to it


### Niche

Advertising

## Set Up and Installation

Clone the repository into your local machine, to install this project, using the following command;
                
                git clone https://github.com/capinho/Qrcodeapp.git

After cloning, change directory into the project folder, using the command below;

                cd <project-directory>
                
Create a virtual environment (unarguably a very useful practice for new projects) to install the required dependencies, using; 

                virtualenv <virtual-environment-name>
                 
Activate the virtual environment you created using;              
  
    Linux/OS: 
   
                $ source <virtual-environment-name>/Scripts/activate
              
    Windows OS:
   
                C:\Users\Name\<project-directory> path\to\<virtual-environment-name>\Scripts\activate
  
Install the required dependencies using;

                pip install -r requirements.txt
                
Prepare the models as tables to be migrated to the database using;
                
                python manage.py makemigrations
                
Migrate the tables using;

                python manage.py migrate
                 
Then run your server using;

                  python manage.py runserver


## Technologies Used


### Frontend - HTML5 

### Backend - Stack: Python 

### Framework - Django 

### Database - SQLite3 <a href="https://www.sqlite.org/index.html" target="_blank" rel="noreferrer"></a>

