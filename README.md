# SERVER DIRECTORY WEBSITE

## Gamer's-verse

## Full stack website

**Built using**:\
Django, Python, JavaScript, BootStrap, CSS and HTML.

**Also including**:\
Cloudinary, SELECT2 and tinyMCE.

## Live Site

Coming soon...

## Repository

[server-directory-website](https://github.com/BobWritesCode/server-directory-website)

---

## Table of Contents

- [Gamer's-verse](#Gamer's-verse)
  - [Live Site](#live-site)
  - [Repository](#repository)
  - [Table of Contents](#table-of-contents)
  - [Objective](#objective)
  - [Brief](#brief)
    - [Gamer's-verse - Server Directory Website](#gamer's-verse-server-directory-website)
  - [UX &#8722; User Experience Design](#ux--user-experience-design)
    - [Site-visitor](#site-visitor)
    - [Server-Owner](#server-owner)
    - [Site Admin](#site-admin)
  - [Initial Concept](#initial-concept)
    - [Wireframes](#wireframes)
    - [Colour Scheme](#colour-scheme)
    - [Typography](#typography)
    - [Imagery](#imagery)
  - [Logic](#logic)
    - [Data Model](#data-model)
    - [Python](#python)
    - [JavaScript](#javascript)
  - [Features](#features)
    - [Existing Features](#existing-features)
    - [Features Left to Implement](#features-left-to-implement)
  - [Data Model](#data-model)
  - [Technologies Used](#technologies-used)
    - [Python Packages](#python-packages)
    - [VS Code Extensions](#vs-code-extensions)
    - [Other Tech](#other-tech)
  - [Testing](#testing)
    - [Extensive Testing](#extensive-testing)
    - [Testers](#testers)
    - [Python](#python)
    - [JavaScript](#javascript)
  - [Bugs](#bugs)
    - [Current](#current)
    - [Resolved](#resolved)
  - [Development](#development)
    - [GitHub - Create new repository from template](#github---create-new-repository-from-template)
    - [GitHub - Cloning](#github---cloning)
    - [Cloudinary](#cloudinary)
    - [Postgres](#postgres)
    - [Heroku](#heroku)
  - [Credits](#credits)
    - [Content](#content)
    - [Media](#media)
    - [Acknowledgements](#acknowledgements)

---

## Objective

Design a Full-Stack site based on business logic used to control a centrally-owned dataset. I will need to set up an authentication mechanism and provide role-based access to the site's data or other activities based on the dataset.

**Main Technologies that need to be used**:\
HTML, CSS, JavaScript, Python+Django
Relational database (recommending MySQL or Postgres)

## Brief

### Gamer's-verse - Server Directory Website

The goal of this website are:

- to provide a private server directory that users can visit to find a private server based on the game they wish to find that server on.
- for server owners to be able to list their own server to be found by potential players.
- to have a front-end admin access section that allows "staff" to moderate listings. As well as manage users, listings, games and tags.

---

## UX &#8722; User Experience Design

Some example user stories which will affect the design and project functionality.

### Site-visitor

> *"As a site user there is a easy to navigate homepage so that I can get to the correct part of the website without confusion."*
>
> *"As a new site user I can sign up so that access member only features like creating a server listing."*
>
> *"As a site-user I can login so that access my profile and make changes."*
>
> *"As a site-user I can choose a game from list of games on the homepage so that I can see all the private servers available for that game."*
>
> *"As a site-user I want the server list to show only servers for the game I selected on the homepage so that I don't get confused with servers appearing from games I did not select."*
>
> *"As a site-user I can click on a server in the server list so that I can see full details of that server in a new page."*
>
> *"As a site user I can like a server so that other users can see what servers receive positive feedback."*
>
> *"As a site user I can filter my search results so that I can narrow down my choices to be more specific."*
>
> *"As a site user I can filter my search results so that I can narrow down my choices to be more specific."*
>
> *"As a site user I can search the directory so that I can see a list of server that may interest me."*
>

### Server-Owner

> *"As a server owner I can list my server in the directory so that potential new players will be able to find my server."*
>
> *"As a server owner I can delete my server listening so that it is no longer available to republished."*
>
> *"As a server owner I can update my server listening so that I can make sure that the latest information is available all the time."*
>
> *"As a server owner I can apply tags so that site users can more easily can my server that may interest them."*
>
> *"As a server owner I can upload images for my server profile so that site users can get a better feel for my server."*

### Site Admin

> *"As a site admin I can manually feature a listening so that they get extra awareness."*
>
> *"As a site admin I want to be able to manage the site from a user-friendly admin panel."*

---

## Initial Concept

### Wireframes

Below are some wireframe that I designed to help build and represent the design of the website.

#### Homepage - PC

![Homepage](./README_Images/wireframe_homepage.png)

#### Homepage - Mobile

![Homepage on mobile](./README_Images/wireframe_homepage_mobile.png)

#### Listings - PC

![Listings](./README_Images/wireframe_listings.png)

#### Listings - Mobile

![Listings on mobile](./README_Images/wireframe_listings_mobile.png)

#### Full listing - PC

![Full listing](./README_Images/wireframe_full_listing.png)

#### Full listing - Mobile

![Full listing on mobile](./README_Images/wireframe_full_listing_mobile.png)

#### My Account - PC

![My Account](./README_Images/wireframe_my_account.png)

#### My Account - Mobile

![My Account on mobile](./README_Images/wireframe_my_account_mobile.png)

#### Create Listing - PC

![Create Listing](./README_Images/wireframe_create_listing.png)

#### Create Listing - Mobile

![Create Listing on mobile](./README_Images/wireframe_create_listing_mobile.png)

### Colour Scheme

The 4 main colour's hex codes for this site are: D63600, F8F9FA, 262626, 151515.\
This 4 colours contrast very nicely against each other, and the white text against the other 3 colours pass WCAG contrast scores.

![Colour scheme site example](./README_Images/colour_scheme_text_example.png)

![Colour scheme](./README_Images/colour_scheme.png)

### Typography

### Imagery

---

## Logic

### Data Model

The below entity relationship diagram (ERD) is a graphical representation that depicts relationships between the different models in this project. It also shows the different attributes and their types for each class.

![Entity relationship diagram (ERD)](./README_Images/erd.png)

### Python

### JavaScript

---

## Features

### Existing Features

#### Select2

[Select2](https://select2.org/)

#### tinyMCE

[tinyMCE](https://django-tinymce.readthedocs.io/en/latest/)

### Sending email verification

To help me get this set up, I followed this [guide](https://shafikshaon.medium.com/user-registration-with-email-verification-in-django-8aeff5ce498d).

There were some changes to be made due to potentially using newer version of Django.

Instead of using `EmailMessage()`, I used `send_mail()`.

```python
# ORIGINAL CODE
email = EmailMessage(
    subject=mail_subject,
    body=message,
    to=[to_email]
)
email.send()
```

```python
# NEW CODE
send_mail(
    subject=mail_subject,
    message=message,
    from_email='contact@warwickhart.com',
    recipient_list=[to_email]
)
```

### Features Left to Implement

---

## Data Model

---

## Technologies Used

### Python Packages

#### datetime

pip install datetime

#### django-apscheduler

pip install django-apscheduler

### VS Code Extensions

### Other Tech

---

## Testing

### Extensive Testing

### Testers

### Python

### JavaScript

---

## Bugs

### Current

### Resolved

---

## Development

### GitHub - Create new repository from template

### GitHub - Cloning

### Cloudinary

### Postgres

### Heroku

---

## Credits

### Content

### Media

### Acknowledgements
