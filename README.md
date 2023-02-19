# SERVER DIRECTORY WEBSITE

## Gamer's-verse

## Full stack website

**Built using**:\
Django, Python, JavaScript, BootStrap, CSS and HTML.

**Also including**:\
Cloudinary, SELECT2 and tinyMCE.

## Live Site

[Hosted on Herokuapp](https://server-directory-website.herokuapp.com/)

## Repository

[GitHub repository](https://github.com/BobWritesCode/server-directory-website)

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
  - [Development](#initial-concept)
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

## Development

### Wireframes

Below are some wireframe that I designed to help build and represent the design of the website.

#### Homepage design

<details><summary>PC</summary> <!-- markdownlint-disable-line -->

![Homepage](./README_Images/wireframe_homepage.png)
</details>
<details><summary>Mobile</summary> <!-- markdownlint-disable-line -->

![Homepage on mobile](./README_Images/wireframe_homepage_mobile.png)
</details>

#### Listings design

<details><summary>PC</summary> <!-- markdownlint-disable-line -->

![Listings](./README_Images/wireframe_listings.png)
</details>
<details><summary>Mobile</summary> <!-- markdownlint-disable-line -->

![Listings on mobile](./README_Images/wireframe_listings_mobile.png)
</details>

#### Full listing design

<details><summary>PC</summary> <!-- markdownlint-disable-line -->

![Full listing](./README_Images/wireframe_full_listing.png)
</details>
<details><summary>Mobile</summary> <!-- markdownlint-disable-line -->

![Full listing on mobile](./README_Images/wireframe_full_listing_mobile.png)
</details>

#### My Account design

<details><summary>PC</summary> <!-- markdownlint-disable-line -->

![My Account](./README_Images/wireframe_my_account.png)
</details>
<details><summary>Mobile</summary> <!-- markdownlint-disable-line -->

![My Account on mobile](./README_Images/wireframe_my_account_mobile.png)
</details>

#### Create Listing design

<details><summary>PC</summary> <!-- markdownlint-disable-line -->

![Create Listing](./README_Images/wireframe_create_listing.png)
</details>
<details><summary>Mobile</summary> <!-- markdownlint-disable-line -->

![Create Listing on mobile](./README_Images/wireframe_create_listing_mobile.png)
</details>

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

*Created using: [app.diagrams.net](https://app.diagrams.net)*

### Python

### JavaScript

---

## Features

### Existing Features

#### Navbar

The navbar was design to be simple and vibrant. Early versions the Navbar was off-white but feedback suggested that it was not completely obvious there was a nav bar as it would tend to merge in with the browser bar if using a PC to access the website.

Depending if the user is flagged as a staff member will determine if they can see the 'Admin' nav button.

<details><summary>PC</summary> <!-- markdownlint-disable-line -->

![Navbar PC](./README_Images/site_navbar_pc.png)
</details>

<details><summary>Mobile</summary> <!-- markdownlint-disable-line -->

![Navbar Mobile](./README_Images/site_navbar_mobile.png)
</details>

```html
<!-- base.html -->
<div class="collapse navbar-collapse" style="flex-grow: unset;" id="navbarTogglerDemo02">
    <ul class="navbar-nav mt-2 mt-lg-0">
        <!-- Here we check to see if the requesting user is logged in -->
        {% if user.is_authenticated %}
        <li class="navbar-text text-light">
            <strong>Hi {{ user.username }}!</strong>
        </li>
        <li class="nav-item">
            <a class="nav-link text-light" href="{% url 'my-account' %}">My Account</a>
        </li>
        <!-- Here we check to see if the requesting user is a staff member -->
        {% if user.is_staff %}
        <li class="nav-item text-light">
            <a class="nav-link text-light" href="{% url 'staff_account' %}">Admin</a>
        </li>
        {% endif %}
        <li class="nav-item text-light">
            <a class="ms-1 me-3 btn btn-outline-light" href="{% url 'logout' %}">Log Out</a>
        </li>
        <!-- If requesting user is not logged in -->
        {% else %}
        <li class="nav-item">
            <a class="ms-1 nav-link text-light" href="{% url 'login' %}">Login</a>
        </li>
        <li class="nav-item">
            <a class="ms-1 me-3 btn btn-outline-light" href="{% url 'signup' %}">Sign Up</a>
        </li>
        {% endif %}
    </ul>
</div>
```

#### Homepage

The homepage is designed to be simple and provide a clear understanding of what the website is about when a first time user visits.

<details><summary>Homepage screenshot</summary> <!-- markdownlint-disable-line -->

![Homepage](./README_Images/site_homepage.png)
</details>

The user can hover their mouse over the different game cards. This help the user understand these are intractable. For UX purpose the whole card was made a clickable link to avoid user confusion on how to proceed.

![Game cards](./README_Images/site_homepage_games.gif)

#### Server listings

The server listing page allows the user to start looking through the different listings. The user can filter their search down using the tags filter on the right. They can select up to as many tags as they like and also easily remove tags. This provides a much more bespoke list that is filled only with that user's interests.

<details><summary>Server listings screenshot</summary> <!-- markdownlint-disable-line -->

![Server listings](./README_Images/site_server_listings.png)
</details>

```py
# views.py
# These are snippets from the code to provide the filtering by essentially
# building tag string in the url. I removed other parts of this method not
# to the tag filtering.

def server_listings(request: object, slug: str, tag_string: str = ""):

    # Get only the tags linked to a game.
    game = get_object_or_404(Game, slug=slug)
    tags = game.tags.all()

    # Create and empty list then append all tags into that list.
    all_tags_for_game = []
    for tag in tags:
        all_tags_for_game.append([tag.pk, tag.name])

    # Manage tag_string
    if tag_string != "":
        # Create list from string
        selected_tags = tag_string.split("%")
        # Check to see if adding or removing tag
        action = selected_tags.pop(0)

        # A = add tag, R = remove tag
        if action == "A":
            # Prepare new tag_string to send to front-end
            tag_string = '%' + '%'.join(selected_tags)

        else:
            # Which tag has been selected to be removed
            to_be_removed = selected_tags.pop(0)

            # Remove tag from selected list
            selected_tags.remove(to_be_removed)

            # Check to see if all tags have been unselected
            # Prepare tag_string
            if len(selected_tags) != 0:
                tag_string = '%' + '%'.join(selected_tags)
            else:
                tag_string = ''

        # Narrows server list down based on tags picked by user
        for value in selected_tags:
            listings = listings.filter(tags__name=value)

        # Use list comprehension to remove selected tags from all
        # available tags
        tags = [x for x in game.tags.all() if x.name not in selected_tags]

        tags.sort(key=operator.attrgetter('name'))
        selected_tags.sort()

    else:
        # If tag_string empty then create empty list
        selected_tags = []
        # Get all available tags for game selected
        tags = game.tags.all().order_by('name')

    # We can now render the page and provide tags, selected_tags and
    # tag_string as context.
```

#### View Listing

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Server listings](./README_Images/site_listing.png)
</details>

The full listing page provides the user a much more detailed insight about the server listing. It allows the server owner to provide a long description so they can describe as much detail as they want about the server to attract new players.

On this page their is a section just under the tags where a user can interact with, here a user can:

- Bump the listing,
- Find the discord invite link,
- Find the TikTok profile link (if available, if not this button will not be shown).

If the user is a staff member then the staff view panel will also be shown, where a staff user can quickly go to the owner's profile or edit the listing.

![Server listings panel](./README_Images/feat_listing_panel.gif)

#### Bumps

![Bumps](./README_Images/feat_bump.gif)

Bumps allow user to help promote a listing. Bumping a server will push it to the top of the listings. And similar to how search engine results work, the higher up the list you are the more views you will get.

To help promote active servers bumps expire after the duration set by the site owner, currently stored in the `constants.py` file, but at a later date there will be an option to be able to change this in a super admin panel. Making it easier for an end user to update themselves.

A user can only bump up to a specific amount of listings at a time, and will have to wait until their bump expires. Currently it is set to expire the next date for the purposes of this project demonstration.

A user can only bump a single list once at a time.
Once a user has used up their allocated bumps they will see a message saying they are out of bumps.
A user has to be signed in to bump otherwise they will see a message saying they need to login first.

![Bump login](./README_Images/feat_bump_login.png) ![Out of bumps!](./README_Images/feat_bump_out_of.png)

This is what the user Bumps list looks like in their [My Account](#my-account) page.

![Bump list](./README_Images/feat_bump_list.png)

The way the bumps are automatically expired is by setting a automated task that run at midnight everyday or at server restart. The task will query for bumps that are less than or, equal to the current date and delete them. Print messages are produced purely as a way to check there are no issues.

*You can read more about how the automated jobs work by checking out the [APScheduler](#django-apscheduler) section of this README.*

```py
#jobs.py
def clear_bumps():
    """
    Automated task: Finds expired bumps and deletes them.
    """
    print('clear_bumps(): Starting automated task.')
    # Get bumps that have expired
    # __lte means 'less than or, equal to', this is used oppose to '<='>
    query = Q(expiry__lte=datetime.now())
    queryset = Bumps.objects.filter(query)
    print(f'clear_bumps(): Deleting {len(queryset)} bump(s).')
    # Delete expired bumps
    queryset.delete()
    print('clear_bumps(): Completed automated task.')
```

#### User Authentication

##### Sign up

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Sign up form](./README_Images/site_signup.png)
</details>

It's important that user's can easily sign up, the sign up form it self is designed to be simplistic. Asking for a username, email address, and password. Email and password will be what is required to login but the username will be used to identify the user to other site users and staff. Both the username and email address have to be unique and the user will be notified if they are not.

![Username already in user](./README_Images/feat_signup_username.png)

![Email already in user](./README_Images/feat_signup_email.png)

```py
# views.py
def sign_up_view(request):
    """
    GET: Loads sign up view
    POST: Attempts to create a new user, unless there is an error
    then displays error to the user.

    Args:
        request (object): GET/POST request from user.

    Returns:
        redirect (function): Email verification view.
        render (function): Loads view.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        # Check user has completed form as required.
        if form.is_valid():
            # Original code before modifications, check ReadMe:
            # https://shafikshaon.medium.com/
            # user-registration-with-email-verification-in-django-8aeff5ce498d
            # Save new user to database.
            try:
                user = form.save()
                send_email_verification(request, user)
                return redirect('signup_verify_email')
            except ValidationError as err:
                for field, errors in err.message_dict.items():
                    form.add_error(field, errors)
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})
```

##### Email verification

Once the user has successfully input the their sign up details they will be directed to a screen explaining that they have been sent an email to verify their email address.

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Verify email address page](./README_Images/site_verify_email_address.png)
</details>

```py
# views.py
def send_email_verification(request: object, user: object):
    '''
    Send email address verification to user.

    Parameters:
        request (object): GET/POST request from user.
        user (object): Target user model object.
    '''
    current_site = get_current_site(request)
    mail_subject = 'Verify your email address.'
    message = render_to_string('email_templates/verify_email_address.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })

    # Send email to user.
    send_mail(
        subject=mail_subject,
        message=message,
        from_email='contact@warwickhart.com',
        recipient_list=[user.email]
    )
```

To make sure your emails send you need to make sure you set up the following settings correctly in your settings.py

```py
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
MAILER_EMAIL_BACKEND = EMAIL_BACKEND
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
```

The user will receive a email notification, you can personalise the email using a template. This is a very basic template but for the purpose of this project serves the projects need's.

```html
{% autoescape off %}
Hi {{ user.username }},

Please click on the link to confirm your registration,

http://{{ domain }}{% url 'activate' uidb64=uid token=token %}

If you think, it's not you, then just ignore this email.

Kind regards
The Gamer's-verse team

{% endautoescape %}
```

![Verification email](./README_Images/feat_signup_email_verify.png)

Once the user visits the link in the email they will be taken to the page to show that their email address is now verified and they can now login.

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Email address verified page](./README_Images/site_signup_email_address_verified.png)
</details>

##### Login

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Login page](./README_Images/site_login.png)
</details>

The login screen as many of us would expect is a nice simple user form to input their email address and password.

If the user cannot be found, or password does not match the correct account they will get a notification them so.

![Login error](./README_Images/feat_login_mismatch.png)

Also if the user has been flagged as banned they will also get told so.

![Login banned](./README_Images/feat_login_banned.png)

Once user has been authenticated they will then be redirected to their [My Account](#my-account) page.

```py
# views.py
def login_view(request: object):
    """
    Login-view and process login.

    Args:
        request (object): GET/POST request from user..

    Returns:
        render(): Loads html page.
    """
    error_message = None

    # If user already logged in, just direct them to My Account page.
    if request.user:
        return redirect("my-account")

    if request.method == 'POST':
        # Get from request user input.
        email = request.POST['email']
        password = request.POST['password']
        # Check credentials are found and a match.
        user = authenticate(request, email=email, password=password)
        if user is None:
            # ERROR: User not found, or password mismatch.
            error_message = (
                "Either user does not exist or password does not "
                "match account."
            )
        else:
            # Check if user is banned.
            if user.is_banned:
                # ERROR: User account has been flagged as banned.
                error_message = "This account is banned."
                user = None
            # All being okay, log user in.
            else:
                login(request, user)
                return redirect("my-account")

    form = LoginForm()

    return render(
        request,
        "registration/login.html",
        {
            "form": form,
            "error_message": error_message,
        },
    )
```

##### Forgotten password

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Forgotten Password page](./README_Images/site_forgotten_password.png)
</details>

At some point a user will forget their password. So I have made sure included within the project is a forgotten password function.

Taking advantage of the Django auth_views class, we can do this with relative ease, assuming that emailing has beet set up

The use will see a password reset confirmation page, to let them know that request has been accepted.

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Forgotten Password confirmation page](./README_Images/site_forgotten_password_part2.png)
</details>

The user will then receive an email with a link to reset their password.

![Password reset email](./README_Images/feat_password_reset_email.png)

After the user visits the link they will be directed to the "Enter new password" page.

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Enter New Password](./README_Images/site_password_reset.png)
</details>

And finally once the user has confirmed their new password, they are presented with the option to login or go to the homepage.

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Enter New Password](./README_Images/site_password_reset_confirm.png)
</details>

```py
# urls.py

path(
    'accounts/password_reset',
    auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html",
        form_class=PasswordResetForm,
        subject_template_name='email_templates/password_reset_subject.txt',
        email_template_name='email_templates/password_reset_email.html',
        success_url='password_reset_done',
    ),
    name='password_reset'
),

path(
    'accounts/password_reset_done',
    auth_views.PasswordResetDoneView.as_view(
    ),
    name='password_reset_done'
),

path(
    'accounts/password_change/',
    auth_views.PasswordChangeView.as_view(
        template_name="registration/password_change_form.html",
        success_url='password_change_done',
        form_class=PasswordChangeForm,
        extra_context={},
    ),
    name='password_change'
),

path(
    'accounts/reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html",
        success_url='password_reset_complete',
        form_class=SetPasswordForm,
        extra_context={},
    ),
    name='password_reset_confirm'
),
```

#### My Account

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![My Account page](./README_Images/site_my_account.png)
</details>

The [My Account](#my-account) is the main hub for a user to mange their profile, see their active bumps, create and manage their listings, and delete their account.

- [Profile](#profile)
- [Email update](#email-update)
- [Password change](#password-change)
- [Delete account](#delete-account)

##### Profile

Starting from the top of the [My Account](#my-account) page and working our way down, the first section is the 'Profile' section. In this section the user can see their username and their current email address. Currently the user cannot update their username but this is something that could be available in a future update.

##### Email update

By clicking on the Update email address button the user will see a modal come up with instructions on how to change their email address.

![Email update modal](./README_Images/feat_email_update_modal.png)

If the user tries to change their email address to an email address already in use, they will receive an error notification.

![Email already in use](./README_Images/feat_email_update_taken.png)

Once the form is completed the user's email address will be updated but the the email address will now be unverified. The user will also be sent an email to verify their new email address just like they did when they originally signed up to the website.

![Unverified email](./README_Images/feat_email_update_unverified.png)

##### Password change

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Password change page](./README_Images/site_password_change.png)
</details>

Takes you to the password change page where the user is required to enter their current password, and then their new password twice.

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Password change page](./README_Images/site_password_change.png)
</details>

All going well, the user will be shown a password change page to confirm the change was successful.

##### Delete account

At the bottom of the [My Account](#my-account) page is the 'Delete account' section. Here the user can completely delete their account which also delete associated listings and bumps.

When the user clicks on the trash can button a modal will come up asking the user to delete their account. As part of **defensive programming**, to stop the user accidentally performing a irreversible action, the user actually needs to input a phrase into the input box before be able to finalise the action.

![Delete account modal](./README_Images/feat_delete_account.png)

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Account deleted page](./README_Images/site_account_deleted.png)
</details>
Finally the user is taken an 'Account Deleted' page to confirm the account has been removed from the database.

---

### Listings

[Go to top.](#server-directory-website)

The core of the website is of course the ability for server owners to list their private servers and for players to find a new server to join.

- [Create Listing](#create-listing)
- [My Listing](#my-listings)
- [Edit Listing](#edit-listing)
- [Delete Listing](#delete-listing)

#### Create Listing

Once a user has signed up and logged in they can go to [My Account](#my-account) and scroll down to 'Your Listings' and click the button to 'Create Listing'.

![Create Listing Button](./README_Images/site_create_listing_button.gif)

The user can currently create up to 3 listings. But in future feature this will be something that the site-owner will be able to adjust in the front end.

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Create Listing page](./README_Images/site_create_listing.png)
</details>

On the create listing page the user will be need complete all the mandatory fields. This page also includes two widgets that are not part of Django. They are:

- [Select2](#select2) for the tags dropdown, and,
- [TinyMCE](#tinymce) for the short and long description boxes.

The image upload is done via [Cloudinary](#cloudinary).

If the user tries to submit the form uncompleted they will receive error messages to let hem know, and the page will automatically scroll back to the top, just so the user can see something happened after pressing the submit button.

![Create Listing error](./README_Images/feat_create_listing_error.png)

Once the form has been completed correctly and submitted the new listing will be saved to the database. And the user will be able to see and manage the listing from their [My Account](#my-account) page.

#### My Listings

Of course, once a user has created a listing, we need to let them be able to manage that listing. Which we do from the [My Account](#my-account) page.

![My Listings](./README_Images/feat_your_listings.png)

Each listing shows the user:

- The uploaded image, including [image review](#image-review) status:
  - Awaiting Approval,
  - Approved,
  - Rejected:
    - Rejected images are automatically deleted after a certain time.
  - If no image uploaded there will be a placeholder saying 'Awaiting image'.
- Server name,
- Tags,
- Short description,
- Management panel.

##### My Listings management panel

This panel allows the user quick access to options to help manage their listing. The panel includes:

- View if listing status is to published or draft,
- View active [bumps](#bumps),
- Go to [live listing](#view-listing).
- Go to [edit listing](#edit-listing).
- Delete listing.

![My Listings management panel](./README_Images/feat_my_listings_panel.gif)

##### Edit Listing

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Edit Listing page](./README_Images/site_edit_listing.png)
</details>

The view is very similar to [create listing](#create-listing) view but with the added extra elements of seeing the current uploaded image (which can be replaced), and the [delete listing](#delete-listing) button at the bottom of the page.

##### Delete Listing

If the user tries to delete a listing, as this is permanent and irreversible process, defensive programming has been implemented.  When the user click the delete listing button a modal will open which requires the user to type a specific phrase before the operation will be completed.

![Delete listing modal](./README_Images/feat_delete_listing_modal.png)

Once the user completes the instructions the listing, and image will be deleted from the database.

---

### Admin Account Page

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Admin Account Page](./README_Images/site_admin_account_page.png)
</details>

It is important to have a front-end user friendly interface for the site owner and allocated staff members to manage the day-to-day aspects of the site.

The [admin account page](#admin-account-page) currently has the following features:

- [Image Review](#image-review)
- [Manage Users](#manage-users)
- [Manage Games](#manage-games)
- [Manage Tags](#manage-tags)

---

### Image Review

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Image Review Page](./README_Images/site_image_review.png)
</details>

The image review page allows staff members to check images that have been uploaded by users before they can be seen publicly. This is a safety precaution to make sure images that would be against the site's terms of service are not being displayed.

Every image to be reviewed will has 4 options:

- Approve,
  - Makes the image public.

    ```py
    # views.py
    item = get_object_or_404(Images, pk=content[1])
    item.status = 1
    item.expiry = None
    item.reviewed_by = request.user
    item.save()
    ```

- Reject,
  - Will set the image for deletion after 3 days.

    ```py
    # views.py
    item = get_object_or_404(Images, pk=content[1])
    item.status = 2
    item.expiry = date.today() + timedelta(
        days=DAYS_TO_EXPIRE_IMAGE)
    item.reviewed_by = request.user
    item.save()
    ```

- Ban use,
  - Will flag the user as banned, set all images by user as rejected. To stop accidentally trigger this, a modal will appear asking the user to type a specific phrase to complete the operation.

    ```py
    # views.py
    item = get_object_or_404(Images, pk=content[1])
    item.status = 3
    item.expiry = date.today() + timedelta(
        days=DAYS_TO_EXPIRE_IMAGE)
    item.reviewed_by = request.user
    item.save()
    ban_user(request, item.user_id)
    ```

- Next.
  - Will take the user to the next image to be reviewed, and no new images to be reviewed they will be taken back to the [admin account page](#admin-account-page).

    ```py
    query = Q(status=0)
    image_count = Images.objects.filter(query).count()
    # If no image is currently waiting be approved,
    # then handle request.
    if image_count > 0:
        return redirect('staff_image_review')
    else:
        return redirect('staff_account')
    ```

---

### Manage Users

Another crucial feature of the website is the ability for staff user's to be able to find user's and manage them. The Manage user section has many sub-features to it, including:

- [User Search](#user-search)
- [User Management Page](#user-management-page)
- [Updating user](#updating-user)
- [Ban/Unban user](#banunban-user)
- [Send user verification email](#send-user-verification-email)
- [Assign/Resign as staff](#assignresign-as-staff)
- [Delete user](#delete-user)
- [See user listings](#see-user-listings)

#### User Search

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![User Search Page](./README_Images/site_user_search.png)
</details>

This is a simple search, which will allow the user to search for another using using either id, username or email address.

The results are limited to the first 100 in case the database grows significantly.

This python codeblock is an email of the email search getting the first 100 users it finds that match the email string input by the user in the front end.

```py
query = Q(email__contains=content[1])
# Limited to first 100 results.
users = CustomUser.objects.filter(query)[:100]
result = {
    'success': True,
    'users': serializers.serialize('json', users),
}
```

This JavaScript codeblock is that the DOM being updated with the returned results.

```js
/**
 * Performs a promise using askServer() to return a json.
 * @param {object} users Receives users as an object from action(). Then converts
 * them into rows and appends them into a html table.
 */
function displayUsers(users) {
  const tableBody = $('#user-search-display-table tbody');
  tableBody.empty();
  for (let i = 0; i < users.length; i += 1) {
    const user = users[i];
    const row = $('<tr>').appendTo(tableBody);
    $('<th>', { scope: 'row', text: i + 1 }).appendTo(row);
    $('<td>')
      .append(
        $('<a>', {
          href: `staff_user_management_user/${user.pk}`,
          class: 'text-decoration-none link-light',
          text: user.pk,
        }),
      )
      .appendTo(row);
    $('<td>')
      .append(
        $('<a>', {
          href: `staff_user_management_user/${user.pk}`,
          class: 'text-decoration-none link-light',
          text: user.fields.username,
        }),
      )
      .appendTo(row);
    $('<td>')
      .append(
        $('<a>', {
          href: `staff_user_management_user/${user.pk}`,
          class: 'text-decoration-none link-light',
          text: user.fields.email,
        }),
      )
      .appendTo(row);
  }
}
```

The user can then click on any of the results to go to the user management screen.

#### User Management Page

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![User Management Page](./README_Images/site_user_management.png)
</details>

This view allows the user to update other user from one page. Within this one view the user can see the user's attributes, perform actions, and review the user's listings.

For managing the user settings there is a management control panel

**IMPORTANT**: That the assign/resign staff member button only appears for superusers.

**IMPORTANT**: When the target user is a superuser, only other superusers can manage them.

*Management control panel when no restrictions apply:*
![User Management Page](./README_Images/feat_user_management_panel.gif)

*Panel when target user is a superuser but user is not:*
![User Management Page](./README_Images/feat_managment_panel_superuser.png)

#### Updating User

Users can update username, email address and if account is active. After making any changes the user needs to click on the 'Save' icon in the control panel.

If 'Account Active?' is unchecked and the user saved, that user will no longer be able to [login](#login). And they will not receive any message to indicate that there account has been made inactive. Where as a banned user will get a message notifying their account is banned on a [login](#login) attempt.

Once successfully the page will refresh and the new details stored in the database.

#### Ban/Unban User

There is a ban/unban function within the control panel.

Banning a user will:

- Prohibit them from logging in,
- Sign them out from any current sessions,
- Set all their uploaded images for deletion,
- Unpublish any listings they may have.

As this function performs major actions, defensive programming is implemented here, a modal opens and the user needs to type a specific phrase to complete the operation.

Pressing the same button on the control panel on a banned user will unban them.

![Ban modal](./README_Images/feat_ban_modal.png)

```py
def ban_user(request: object, _id: int):
    """
    Bans user and prevents user login, rejects all images for deletion,
    unpublish listings.

    Decorators:
        @login_required: User required to be logged in
        @staff_member_required: Logged in user must be staff.

    Parameters:
        request (object): GET/POST request from user.#
        _id (int): Target user to be banned.
    """
    # Get target user.
    user = get_object_or_404(CustomUser, pk=_id)

    # Delete all current user sessions (in case logged in on multiple devices)
    for session in Session.objects.all():
        if session.get_decoded().get('_auth_user_id') == user.pk:
            session.delete()

    # Flag user as banned.
    user.is_banned = True
    user.save()

    # Unpublish all listings
    query = Q(owner_id=_id)
    ServerListing.objects.filter(query).update(status=0)

    # Unpublish all images and set for deletion
    query = Q(user_id=_id)
    image_expire = date.today() + timedelta(days=DAYS_TO_EXPIRE_IMAGE)
    Images.objects.filter(query).update(status=3, expiry=image_expire)
```

#### Send user verification email

If a staff member updates an email address on a user's behalf, to make sure that the email address belongs to them they send a [verification email](#email-verification) to them. The email will contain a link to confirm that they have access to the email address provided.

![Email verify modal](./README_Images/feat_veri_email_modal.png)

On sending the email, the user's account email_verified will be changed to False.

```py
# Let's see if the user is trying to send a email verification
# to the target user.
if "email-verify" in request.POST:
    user.email_verified = False
    user.save()
    # Send email verification to the user
    send_email_verification(request, user)
    return redirect(
        "staff_user_management_user", _id=request.POST['id']
        )
```

#### Assign/Resign as staff

**IMPORTANT**: This function is only available to superusers.

Allow the superuser to easily assign target user's as staff members or resign them as a staff member.

![Promote staff modal](./README_Images/feat_staff_promote_modal.png)

![Demote staff modal](./README_Images/feat_staff_demote_modal.png)

```py
def promote_user_to_staff(request: object, target_id: int):
    """
    Promotes target user to staff member.

    Args:
        request (object): GET/POST request from user.
        target_id (int): Target user ID.
    """
    # Check request user has correct level before proceeding
    if request.user.is_superuser:
        # Get target user object.
        user = get_object_or_404(CustomUser, id=target_id)
        # Change flag.
        user.is_staff = True
        # Save user.
        user.save()


def demote_user_from_staff(request: object, target_id: int):
    """
    Demote target user as staff member.

    Args:
        request (object): GET/POST request from user.
        target_id (int): Target user ID.
    """
    # Check request user has correct level before proceeding
    if request.user.is_superuser:
        # Get target user object.
        user = get_object_or_404(CustomUser, id=target_id)
        # Change flag.
        user.is_staff = False
        # Save user.
        user.save()
```

#### Delete user

This function allows a staff user to delete a target user from the database.

![Demote staff modal](./README_Images/feat_delete_user_modal.png)

#### See user listings

---

### Manage Games

#### Adding a game

#### Updating a game

---

### Manage Tags

#### Adding a tag

#### Updating a tag

---

#### Cloudinary

#### Select2

[Select2 website](https://select2.org/)

#### tinyMCE

[tinyMCE website](https://django-tinymce.readthedocs.io/en/latest/)

### Sending email verification

To help me get this set up, I followed this [guide](https://shafikshaon.medium.com/user-registration-with-email-verification-in-django-8aeff5ce498d).

There were some changes to be made due to potentially using newer version of Django.

Instead of using `EmailMessage()`, I used `send_mail()`.

```py
# ORIGINAL CODE
email = EmailMessage(
    subject=mail_subject,
    body=message,
    to=[to_email]
)
email.send()
```

```py
# NEW CODE
send_mail(
    subject=mail_subject,
    message=message,
    from_email='contact@warwickhart.com',
    recipient_list=[to_email]
)
```

### Features Left to Implement

Site owner change:

- when bumps bumps expire.
- how many bumps a user can have active at a time.
- change the amount of listings a person can list at once.

Staff:

- Be able to review already approved images via image ID

UX

- Add success messages when data is updated.

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

### Postgres

### Heroku

---

## Credits

### Content

### Media

### Acknowledgements
