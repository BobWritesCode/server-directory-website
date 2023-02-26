# SERVER DIRECTORY WEBSITE

## Gamer's-verse

## Full Stack Website

**Built using**:\
Django, Python, JavaScript, BootStrap, CSS and HTML.

**Also including**:\
Cloudinary, Select2 and tinyMCE.

## Live Site

[Hosted on Heroku](https://server-directory-website.herokuapp.com/)

## Repository

[GitHub repository](https://github.com/BobWritesCode/server-directory-website)

## Table Of Contents

- [Gamer's-verse](#gamers-verse)
  - [Live Site](#live-site)
  - [Repository](#repository)
  - [Table of Contents](#table-of-contents)
  - [Objective](#objective)
  - [Brief](#brief)
    - [Gamer's-verse - Server Directory Website](#gamers-verse---server-directory-website)
  - [UX - User Experience Design](#ux---user-experience-design)
    - [Site-visitor](#site-visitor)
    - [Server-Owner](#server-owner)
    - [Site-Admin](#site-admin)
  - [Development](#development)
    - [Agile Design](#agile-design)
      - [GitHub Issues](#github-issues)
        - [Issue numbers](#issue-numbers)
        - [User Story](#user-story)
        - [Bug Report](#bug-report)
        - [Feature Request](#feature-request)
        - [Improvement Request](#improvement-request)
        - [Assign an assignee or assignees](#choose-assignees)
        - [Apply labels](#choose-labels)
        - [Choose the project](#choose-project)
        - [Choose the milestone](#choose-milestone)
      - [Kanban Board](#kanban-board)
    - [Wireframes](#wireframes)
      - [Homepage Design](#homepage-design)
      - [Listings Design](#listings-design)
      - [Full Listing Design](#full-listing-design)
      - [My Account Design](#my-account-design)
      - [Create Listing Design](#create-listing-design)
    - [Colour Scheme](#colour-scheme)
    - [Typography](#typography)
    - [Imagery](#imagery)
  - [Features](#features)
    - [Existing Features](#existing-features)
      - [Navbar](#navbar)
      - [Homepage](#homepage)
      - [Listings](#listings)
        - [Tag Strings](#tag-strings)
      - [View Listing](#view-listing)
      - [Bumps](#bumps)
      - [User Authentication](#user-authentication)
        - [Sign Up](#sign-up)
        - [Email verification](#email-verification)
        - [Login](#login)
        - [Forgotten password](#forgotten-password)
      - [My Account](#my-account)
        - [Profile](#profile)
        - [Email Update](#email-update)
        - [Password Change](#password-change)
        - [Delete Account](#delete-account)
        - [Listings](#listings)
          - [Create Listing](#create-listing)
          - [Your Listings](#your-listings)
            - [Your Listings - Management Panel](#your-listings---management-panel)
          - [Edit Listing](#edit-listing)
          - [Delete Listing](#delete-listing)
      - [Admin Account Page](#admin-account-page)
        - [Image Review](#image-review)
        - [Manage Users](#manage-users)
          - [User Search](#user-search)
          - [User Management Page](#user-management-page)
            - [Updating User](#updating-user)
            - [Ban/Unban User](#banunban-user)
            - [Send User Verification Email](#send-user-verification-email)
            - [Assign/Resign As Staff](#assignresign-as-staff)
            - [Delete User](#delete-user)
            - [See User's Listings](#see-users-listings)
        - [Manage Games](#manage-games)
          - [Adding A Game](#adding-a-game)
          - [Updating A Game](#updating-a-game)
        - [Manage Tags](#manage-tags)
          - [Adding A Tag](#adding-a-tag)
          - [Updating A Tag](#updating-a-tag)
    - [Features Left to Implement](#features-left-to-implement)
  - [Technologies Used](#technologies-used)
    - [Logic](#logic)
      - [Data Model](#data-model)
      - [Django](#django)
      - [Python](#python)
        - [Python Packages](#python-packages)
          - [DateTime](#datetime)
          - [APScheduler](#apscheduler)
          - [Django Crispy Forms](#django-crispy-forms)
      - [JavaScript](#javascript)
        - [JQuery](#jquery)
      - [CSS](#css)
        - [BootStrap](#bootstrap)
    - [Widgets](#widgets)
      - [Cloudinary](#cloudinary)
      - [Select2](#select2)
      - [tinyMCE](#tinymce)
  - [Testing](#testing) (OUTSTANDING)
    - [HTML](#html-testing)
    - [CSS](#css-testing)
    - [JavaScript](#javascript-testing)
    - [Python](#python-testing) (OUTSTANDING)
      - [Linters](#python-linters)
      - [Unit Testing](#unit-testing) (OUTSTANDING)
      - [Coverage](#coverage) (OUTSTANDING)
    - [User Testing](#user-testing) (OUTSTANDING)
  - [Bugs](#bugs)
    - [Unresolved](#unresolved)
    - [Resolved](#resolved)
  - [Deployment](#development)
    - [GitHub - Cloning](#github---cloning)
    - [TinyMCE Deployment](#tinymce-deployment)
    - [Cloudinary Deployment](#cloudinary-deployment)
    - [ElephantSQL Deployment](#elephantsql-deployment)
    - [Heroku](#heroku)
  - [Credits](#credits)
    - [VS Code Extensions](#vs-code-extensions)
    - [Other Tech](#other-tech)
    - [Content](#content)
    - [Acknowledgements](#acknowledgements)

---

## Objective

Design a Full-Stack site based on business logic used to control a centrally-owned dataset. I will need to set up an authentication mechanism and provide role-based access to the site's data or other activities based on the dataset.

**Main Technologies that need to be used**:\
HTML, CSS, JavaScript, Python+Django
Relational database (recommending MySQL or Postgres)

[Back to top🔝](#table-of-contents)

---

## Brief

### Gamer's-verse - Server Directory Website

The goal of this website are:

- to provide a private server directory that users can visit to find a private server based on the game they wish to find that server on.
- for server owners to be able to list their own server to be found by potential players.
- to have a front-end admin access section that allows "staff" to moderate listings. As well as manage users, listings, games and tags.

[Back to top🔝](#table-of-contents)

---

## UX - User Experience Design

Some example user stories which will affect the design and project functionality.

### Site-Visitor

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

### Site-Admin

> *"As a site admin I can manually feature a listening so that they get extra awareness."*
>
> *"As a site admin I want to be able to manage the site from a user-friendly admin panel."*

[Back to top🔝](#table-of-contents)

---

## Development

### Agile Design

- [GitHub Issues](#github-issues)
  - [User Story](#user-story)
  - [Bug Report](#bug-report)
  - [Feature Request](#feature-request)
  - [Improvement Request](#improvement-request)
  - [Assign an assignee or assignees](#choose-assignees)
  - [Apply labels](#choose-labels)
  - [Choose the project](#choose-project)
  - [Choose the milestone](#choose-milestone)
- [Kanban Board](#kanban-board)

When taking on any project especially large and complicated projects with different moving parts, where it's easy to jump from one part of the project to another, leaving the previous part incomplete and leaving room for error. It's best to come up with a strategy. This is where agile design comes in, it can help you identify all the different parts of the project that need to be completed, in which order may be best, and if you are in a team delegate tasks to people so everyone knows what their responsibilities are.

As part of the project, I heavily used GitHub Issues and GitHub Kanban board.

[🔝](#table-of-contents)

#### GitHub Issues

- [Issue numbers](#issue-numbers)

I created 4 different templates for issues being raised:

- [User Story](#user-story)
- [Bug Report](#bug-report)
- [Feature Request](#feature-request)
- [Improvement Request](#improvement-request)

Each issue category played a part in helping easily identify the category the issue was going to be related to, and each has a different template for myself, and other users to provide useful information that will help resolve the issue.

When an issue is either being created or after. There are a few different options you can modify to help delegate the task and its priority. You can:

- [Assign an assignee or assignees](#choose-assignees)
- [Apply labels](#choose-labels)
- [Choose the project](#choose-project)
- [Choose the milestone](#choose-milestone)

[Back to top🔝](#table-of-contents)

##### Issue numbers

Every issue raised will have an issue number i.e., #1, #2, #3 and so on. If you put the issue number in the commit message, then that commit will automatically by GitHub be linked to that issue.

If you use certain keywords as well it will also automatically manage the issue such as 'bug: fixes #58'. This will automatically close that issue for you.

##### User Story

[Link to User Story template.](https://github.com/BobWritesCode/server-directory-website/blob/master/.github/ISSUE_TEMPLATE/user-story.md)

[Link to User Story Issues.](https://github.com/BobWritesCode/server-directory-website/issues?q=is%3Aissue+%5BUser+Story%5D+)

The User Story was the first template I created, and this was basically to help start to build the idea of the project and what potential features were going to be needed.

Any User Story was also allocated the tag 'enhancement' automatically to help identify this was going to be a new feature.

##### Bug Report

[Link to Bug Report template.](https://github.com/BobWritesCode/server-directory-website/blob/master/.github/ISSUE_TEMPLATE/bug_report.md)

[Link to Bug Report Issues.](https://github.com/BobWritesCode/server-directory-website/issues?q=is%3Aissue+label%3Abug)

As this is a larger and more complicated project, inevitably bugs came up. Bugs are very easy to get distracted by as they generally were discovered while I was working on an unrelated feature. When a bug came up, I would create a bug report so I could attend to it later.

Any Bug Report was also allocated the tag 'bug' to help identify this was going to be a new feature. I could also opt to allocate it the tag 'priority' to show it was something that needed to be fixed immediately as it could be either project breaking or may affect many users.

##### Feature Request

[Link to Feature Request template.](https://github.com/BobWritesCode/server-directory-website/blob/master/.github/ISSUE_TEMPLATE/improvement-request.md)

[Link to Feature Request Issues.](https://github.com/BobWritesCode/server-directory-website/issues?q=is%3Aissue+%5BNew+Feat%5D+)

While building the project new ideas on new features would come to mind. Some that would potentially be perfect for the first version of the project and some that potentially could be implemented later. Whenever a new feature came to mind, I would complete the Feature Request form.

Any Feature Request was also allocated the tag 'enhancement' automatically to help identify this was going to be a new feature.

##### Improvement Request

[Link toImprovement Request template.](https://github.com/BobWritesCode/server-directory-website/blob/master/.github/ISSUE_TEMPLATE/improvement-request.md)

[Link to Improvement Request Issues.](https://github.com/BobWritesCode/server-directory-website/issues?q=is%3Aissue+label%3AImprovement)

Either while using the project as a user or developing the project. I would realise improvements to feature that had already been built. To separate new features to improvements I created the Improvement Request form. Improvements could mainly be left to later in the project as it was important to make sure that all the main features were implemented first.

Any Improvement Request was also allocated the tag 'enhancement' automatically to help identify this was going to be a new feature.

##### Choose Assignees

[Link to my assigned issues.](https://github.com/BobWritesCode/server-directory-website/issues?q=is%3Aissue+label%3Aenhancement+assignee%3ABobWritesCode)

It may come as no surprise; I am the only person assigned issues on this project. Potentially in the future if the project grows and the team grows past me, then I would be able to assign other team members to tasks.

##### Choose Labels

[Link to label choices for this project.](https://github.com/BobWritesCode/server-directory-website/labels)

When creating an issue from an issue report, a label is automatically allocated but the user or a person looking after the project can choose to assign their own labels. For example, if something needs to be tagged as 'priority'.

##### Choose Project

It's probably obvious but all issues were assigned to this project. But one small feature that may go unnoticed you are able to choose which column on the Kanban board that issue goes to. For people who prefer to use the Kanban board to see what issues where.

##### Choose Milestone

[Link to milestone for this project.](https://github.com/BobWritesCode/server-directory-website/milestones)

A milestone is essentially a marker in the projects journey i.e., Alpha, Beta, Release v1, v2 and so on... For potentially a large project that is based over a year or on-going you maybe decided to allocate features to different quarters of the year. The milestone option allows you to do that. This essentially prioritises which issues need to be dealt with by when.

In my project I created 3 milestones:

- Launch version 1.00
  - These are issues that 100% must be done ready for version 1.00.
- Non-essential for v.100
  - These are issues that would be nice to have done but are mandatory.
- Post 1.00 to do list
  - These are issues that are mainly going to be features that can wait until version 1.00 has been completed and be implements into a future version.

#### Kanban Board

[Link to project kanban board.](https://github.com/users/BobWritesCode/projects/3)

A Kanban board is an agile project management tool that helps visualize tasks. It helps with the day-to-day works flow as you can easily see which tasks need to be completed. With GitHub projects you can have several views of the Kanban board. As you might want to have one for the team, and maybe views for each team member. Or different labels such as bugs or improvements.

[Back to top🔝](#table-of-contents)

---

### Wireframes

Below are some wireframe that I designed to help build and represent the design of the website.

#### Homepage Design

<details><summary>PC</summary> <!-- markdownlint-disable-line -->

![Homepage](./README_Images/wireframe_homepage.png)
</details>
<details><summary>Mobile</summary> <!-- markdownlint-disable-line -->

![Homepage on mobile](./README_Images/wireframe_homepage_mobile.png)
</details>

#### Listings Design

<details><summary>PC</summary> <!-- markdownlint-disable-line -->

![Listings](./README_Images/wireframe_listings.png)
</details>
<details><summary>Mobile</summary> <!-- markdownlint-disable-line -->

![Listings on mobile](./README_Images/wireframe_listings_mobile.png)
</details>

#### Full Listing Design

<details><summary>PC</summary> <!-- markdownlint-disable-line -->

![Full listing](./README_Images/wireframe_full_listing.png)
</details>
<details><summary>Mobile</summary> <!-- markdownlint-disable-line -->

![Full listing on mobile](./README_Images/wireframe_full_listing_mobile.png)
</details>

#### My Account Design

<details><summary>PC</summary> <!-- markdownlint-disable-line -->

![My Account](./README_Images/wireframe_my_account.png)
</details>
<details><summary>Mobile</summary> <!-- markdownlint-disable-line -->

![My Account on mobile](./README_Images/wireframe_my_account_mobile.png)
</details>

#### Create Listing Design

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

We are using [BootStrap's](#bootstrap) native font stack. As it provides a sharp and clear font that works perfectly with the projects overall styling.

[Link to BootStrap's documentation for Native font stack.](https://getbootstrap.com/docs/5.3/content/reboot/#native-font-stack)

### Imagery

The site currently has no media on it other then what is uploaded by users. Currently this is for game cover images which are covered by 'Fair use'. To make sure that no images that would be offensive or cause complications are being publicly shown on the site, there is the [image review](#image-review) function.

[Back to top🔝](#table-of-contents)

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

[Back to top🔝](#table-of-contents)

#### Homepage

The homepage is designed to be simple and provide a clear understanding of what the website is about when a first time user visits.

<details><summary>Homepage screenshot</summary> <!-- markdownlint-disable-line -->

![Homepage](./README_Images/site_homepage.png)
</details>

The user can hover their mouse over the different game cards. This help the user understand these are intractable. For UX purpose the whole card was made a clickable link to avoid user confusion on how to proceed.

![Game cards](./README_Images/site_homepage_games.gif)

[Back to top🔝](#table-of-contents)

#### Listings

The Listing page allows the user to start looking through the different listings. The user can filter their search down using the tags filter on the right. They can select up to as many tags as they like and also easily remove tags. This provides a much more bespoke list that is filled only with that user's interests.

<details><summary>Listings screenshot</summary> <!-- markdownlint-disable-line -->

![Listings](./README_Images/site_Listings.png)
</details>

##### Tag Strings

One challenge I had was that I wanted to create a feature that allowed users to really customise their search by adding and removing tags. I spent a little time on the internet searching through to find the best way to go about this. I even looked at some other sites that I knew that had a filter by tag function. But what I found was that not many people were able to do it, and you could only apply 1 tag at a time.

So, I came up with the below code to create something I call a 'tag string'. Simply what it does is create a URL that that has a long string in it that tells the server which tags to load for the user. Then the tag buttons `href`s will either be prefixed with an 'A' or an 'R' to indicate if this tag is to be added or removed when the user clicks on the button.

In the end it produces exactly what I needed to do, and this code was completely written purely by myself, as I really couldn't find any solutions or help anywhere.

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

[Back to top🔝](#table-of-contents)

#### View Listing

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Listing](./README_Images/site_listing.png)
</details>

The full listing page provides the user a much more detailed insight about the server listing. It allows the server owner to provide a long description so they can describe as much detail as they want about the server to attract new players.

On this page their is a section just under the tags where a user can interact with, here a user can:

- Bump the listing,
- Find the discord invite link,
- Find the TikTok profile link (if available, if not this button will not be shown).

If the user is a staff member then the staff view panel will also be shown, where a staff user can quickly go to the owner's profile or edit the listing.

![Listing panel](./README_Images/feat_listing_panel.gif)

[Back to top🔝](#table-of-contents)

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

*You can read more about how the automated jobs work by checking out the [APScheduler](#apscheduler) section of this README.*

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

[Back to top🔝](#table-of-contents)

### User Authentication

#### Sign Up

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

[Back to top🔝](#table-of-contents)

#### Email Verification

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

[Back to top🔝](#table-of-contents)

#### Login

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

[Back to top🔝](#table-of-contents)

#### Forgotten password

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

[Back to top🔝](#table-of-contents)

### My Account

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![My Account page](./README_Images/site_my_account.png)
</details>

The [My Account](#my-account) is the main hub for a user to mange their profile, see their active bumps, create and manage their listings, and delete their account.

- [Profile](#profile)
- [Email update](#email-update)
- [Password change](#password-change)
- [Delete account](#delete-account)

[Back to top🔝](#table-of-contents)

#### Profile

Starting from the top of the [My Account](#my-account) page and working our way down, the first section is the 'Profile' section. In this section the user can see their username and their current email address. Currently the user cannot update their username but this is something that could be available in a future update.

[Back to top🔝](#table-of-contents)

#### Email Update

By clicking on the Update email address button the user will see a modal come up with instructions on how to change their email address.

![Email update modal](./README_Images/feat_email_update_modal.png)

If the user tries to change their email address to an email address already in use, they will receive an error notification.

![Email already in use](./README_Images/feat_email_update_taken.png)

Once the form is completed the user's email address will be updated but the the email address will now be unverified. The user will also be sent an email to verify their new email address just like they did when they originally signed up to the website.

![Unverified email](./README_Images/feat_email_update_unverified.png)

[Back to top🔝](#table-of-contents)

#### Password Change

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Password change page](./README_Images/site_password_change.png)
</details>

Takes you to the password change page where the user is required to enter their current password, and then their new password twice.

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Password change page](./README_Images/site_password_change.png)
</details>

All going well, the user will be shown a password change page to confirm the change was successful.

[Back to top🔝](#table-of-contents)

#### Delete Account

At the bottom of the [My Account](#my-account) page is the 'Delete account' section. Here the user can completely delete their account which also delete associated listings and bumps.

**Important:** When the user clicks on the trash can button a modal will come up asking the user to delete their account. As part of **defensive programming**, to stop the user accidentally performing a irreversible action, the user actually needs to input a phrase into the input box before be able to finalise the action.

![Delete account modal](./README_Images/feat_delete_account.png)

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Account deleted page](./README_Images/site_account_deleted.png)
</details>
Finally the user is taken an 'Account Deleted' page to confirm the account has been removed from the database.

[Back to top🔝](#table-of-contents)

### Listings

[Go to top.](#server-directory-website)

The core of the website is of course the ability for server owners to list their private servers and for players to find a new server to join.

- [Create Listing](#create-listing)
- [Your Listing](#your-listings)
- [Edit Listing](#edit-listing)
- [Delete Listing](#delete-listing)

[Back to top🔝](#table-of-contents)

#### Create Listing

Once a user has signed up and logged in they can go to [My Account](#my-account) and scroll down to [Your Listing](#your-listings) and click the button to 'Create Listing'.

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

[Back to top🔝](#table-of-contents)

#### Your Listings

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

[Back to top🔝](#table-of-contents)

##### Your Listings - Management Panel

This panel allows the user quick access to options to help manage their listing. The panel includes:

- View if listing status is to published or draft,
- View active [bumps](#bumps),
- Go to [live listing](#view-listing).
- Go to [edit listing](#edit-listing).
- Delete listing.

![My Listings management panel](./README_Images/feat_my_listings_panel.gif)

[Back to top🔝](#table-of-contents)

#### Edit Listing

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Edit Listing page](./README_Images/site_edit_listing.png)
</details>

The view is very similar to [create listing](#create-listing) view but with the added extra elements of seeing the current uploaded image (which can be replaced), and the [delete listing](#delete-listing) button at the bottom of the page.

[Back to top🔝](#table-of-contents)

##### Delete Listing

**Important:** If the user tries to delete a listing, as this is permanent and irreversible process, defensive programming has been implemented.  When the user click the delete listing button a modal will open which requires the user to type a specific phrase before the operation will be completed.

![Delete listing modal](./README_Images/feat_delete_listing_modal.png)

Once the user completes the instructions the listing, and image will be deleted from the database.

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

[Back to top🔝](#table-of-contents)

#### Image Review

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

[Back to top🔝](#table-of-contents)

#### Manage Users

Another crucial feature of the website is the ability for staff user's to be able to find user's and manage them. The Manage user section has many sub-features to it, including:

- [User Search](#user-search)
- [User Management Page](#user-management-page)
- [Updating user](#updating-user)
- [Ban/Unban user](#banunban-user)
- [Send user verification email](#send-user-verification-email)
- [Assign/Resign as staff](#assignresign-as-staff)
- [Delete user](#delete-user)
- [See user's listings](#see-users-listings)

[Back to top🔝](#table-of-contents)

##### User Search

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

[Back to top🔝](#table-of-contents)

##### User Management Page

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

[Back to top🔝](#table-of-contents)

###### Updating User

Users can update username, email address and if account is active. After making any changes the user needs to click on the 'Save' icon in the control panel.

If 'Account Active?' is unchecked and the user saved, that user will no longer be able to [login](#login). And they will not receive any message to indicate that there account has been made inactive. Where as a banned user will get a message notifying their account is banned on a [login](#login) attempt.

Once successfully the page will refresh and the new details stored in the database.

[Back to top🔝](#table-of-contents)

###### Ban/Unban User

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

[Back to top🔝](#table-of-contents)

###### Send User Verification Email

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

[Back to top🔝](#table-of-contents)

###### Assign/Resign As Staff

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

[Back to top🔝](#table-of-contents)

#### Delete User

This function allows a staff user to delete a target user from the database.

**Important:** As this is a major, permanent and irreversible action, defence programming is implemented, the user will need to type a specific phrase to complete the operation.

![Demote staff modal](./README_Images/feat_delete_user_modal.png)

[Back to top🔝](#table-of-contents)

#### See User's Listings

The lower section of view displays the target user's listing, just how you would see your own listings in [Your Listing](#your-listings).

A staff member has the same abilities as a the listing owner to view, edit and delete each listing.

[Back to top🔝](#table-of-contents)

#### Manage Games

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Manage Game page](./README_Images/site_manage_game.png)
</details>

For game management there are two sections. You can either choose a game from the dropdown menu that already exists in the database to update, or click the '+' icon to add a new game to the database.

- [Adding A Game](#adding-a-game),
- [Updating A Game](#updating-a-game).

[Back to top🔝](#table-of-contents)

##### Adding A Game

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Manage Game page - Add game.](./README_Images/site_manage_game_add.png)
</details>

For each game you add you will need to supply:

- Game name
- Choose which tags will be connected to that game.
  - This uses [Select2](#select2) dropdown widget.
  - At least 1 tag must be choose to be able to save the game to the database.
- Upload an image.
  - Image uploaded using [Cloudinary](#cloudinary).
- Choose to publish to game.

The slug is automatically generated by the game title. It also appears live thanks for JavaScript.

Tags needed to be created using the [Manage Tags](#manage-tags) feature.

```js
window.addEventListener('keyup', () => {
  form.find('#id_slug').val(form.find('#id_name').val().replace(/\s+/g, '-').toLowerCase());
});
```

[Back to top🔝](#table-of-contents)

#### Updating A Game

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Manage Game page - Update game.](./README_Images/site_manage_game_update.png)
</details>

Using the [Select2](#select2) dropdown at the top of the page, you can either search or scroll through and choose the game you wish to update. Once you choose it will automatically appear in the lower section of the page. You can do everything you did when you [added the game](#adding-a-game) plus the added feature now to delete the game.

**Important:** As this is a major, permanent and irreversible action, defence programming is implemented, the user will need to type a specific phrase to complete the operation.

![Manage Game page - Delete game modal](./README_Images/feat_delete_game_modal.png)

#### Manage Tags

[Back to top🔝](#table-of-contents)

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Manage tag page - Update tag.](./README_Images/site_manage_tag.png)
</details>

For tag management there are two sections. You can either choose a tag from the dropdown menu that already exists in the database to update, or click the '+' icon to add a new tag to the database.

- [Adding A tag](#adding-a-tag),
- [Updating A tag](#updating-a-tag).

#### Adding A Tag

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Manage tag page - Update tag.](./README_Images/site_manage_tag_add.png)
</details>

For each tag you add you will need to supply:

- Tag name.

The slug is automatically generated by the tag title. It also appears live thanks for JavaScript.

```js
window.addEventListener('keyup', () => {
  form.find('#id_slug').val(form.find('#id_name').val().replace(/\s+/g, '-').toLowerCase());
});
```

[Back to top🔝](#table-of-contents)

#### Updating A Tag

<details><summary>Screenshot</summary> <!-- markdownlint-disable-line -->

![Manage tag page - Update tag.](./README_Images/site_manage_tag_update.png)
</details>

Using the [Select2](#select2) dropdown at the top of the page, you can either search or scroll through and choose the tag you wish to update. Once you choose it will automatically appear in the lower section of the page. You can do everything you did when you [added the tag](#adding-a-tag) plus the added feature now to delete the tag.

**Important:** As this is a major, permanent and irreversible action, defence programming is implemented, the user will need to type a specific phrase to complete the operation.

![Manage tag page - Delete tag modal](./README_Images/feat_delete_tag_modal.png)

[Back to top🔝](#table-of-contents)

---

### Features Left to Implement

**Site owner change:**

- When long until bumps expire.
- How many bumps a user can have active at a time.
- Change the amount of listings a person can list at once.

**Staff:**

- Be able to review already approved images via image ID

**UX:**

- Add success messages when data is updated.

---

## Technologies Used

### Logic

- [Data Model](#data-model)
- [Django](#django)
- [Python](#python)
  - [Python Packages](#python-packages)
    - [DateTime](#datetime)
    - [APScheduler](#apscheduler)
    - [Django Crispy Forms](#django-crispy-forms)
- [JavaScript](#javascript)
  - [JQuery](#jquery)
- [CSS](#css)
  - [BootStrap](#bootstrap)

[Back to top🔝](#table-of-contents)

#### Data Model

The below entity relationship diagram (ERD) is a graphical representation that depicts relationships between the different models in this project. It also shows the different attributes and their types for each class.

![Entity relationship diagram (ERD)](./README_Images/erd.png)

*Created using: [app.diagrams.net](https://app.diagrams.net)*

#### Django

[Django website](https://www.djangoproject.com/)

The core framework of this project is Django.

As Django put it:

"Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source."

You can follow the [Django tutorial on creating your first app](https://docs.djangoproject.com/en/4.1/intro/tutorial01/).

#### Python

[Python website](https://www.python.org/)

#### Python Packages

Here are a list of packages used in this project and how to install them.

- [DateTime](#datetime)
- [APScheduler](#apscheduler)
- [Django Crispy Forms](#django-crispy-forms)

#### datetime

[Documentation for datatime](https://apscheduler.readthedocs.io/en/3.x/)

datetime is an object-oriented interface to dates and times with similar functionality to the `time` module.

**Set up:**

To install in the terminal use: `pip install datetime`.

#### APScheduler

[Documentation for APScheduler](https://docs.python.org/3/library/datetime.html)\
[Documentation for django-apscheduler](https://pypi.org/project/django-apscheduler/)

This project uses APSchedule to run regular jobs server side to clear user bumps and remove expired images from Cloudinary storage.

**Set up:**

To install in the terminal use:  `pip install apscheduler` and `pip install django-apscheduler`.

In `apps.py` we need to add this code block app class, like so:

```py
# apps.py
# This should already be there.
class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

        # Add this.
        def ready(self):
            from website import updater
            updater.start()
            from website import jobs
            jobs.daily_jobs()
```

This initiate the methods.

We also need to create a `updater.py` and add it into our app. And include the following code:

```py
# updater.py
"""
Initiates task intervals.
Tasks found in jobs.py
"""
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import daily_jobs


def start():
    """ Run when project starts """
    scheduler = BackgroundScheduler()
    # add_job() Runs at midnight every night.
    scheduler.add_job(daily_jobs, 'cron', hour='0')
    scheduler.start()
```

This creates a cron for our tasks to run at midnight every night.

And also we need a `jobs.py` within our app with the following code:

```py
# jobs.py
"""
Automated task to be completed.
Initiated by updater.py
"""
from datetime import datetime
from django.db.models import Q
from cloudinary import uploader
from .models import Bumps, Images


def daily_jobs():
    """
    Lists functions that are run daily or at each server start.

    Decorators:
        None

    Args:
        None

    Returns:
        None
    """
    clear_bumps()
    delete_rejected_images()


def clear_bumps():
    """
    Automated task: Finds expired bumps and deletes them.

    Decorators:
        None

    Args:
        None

    Returns:
        None
    """
    print('clear_bumps(): Starting automated task.')
    # Get bumps that have expired
    query = Q(expiry__lte=datetime.now())
    queryset = Bumps.objects.filter(query)
    print(f'clear_bumps(): Deleting {len(queryset)} bump(s).')
    # Delete expired bumps
    queryset.delete()
    print('clear_bumps(): Completed automated task.')


def delete_rejected_images():
    """
    Automated task: Finds rejected and expired images and delete
    from the Cloudinary server.

    Decorators:
        None

    Args:
        None

    Returns:
        None
    """
    print('delete_rejected_images(): Starting automated task.')
    # Get images that have been marked as rejected and expired
    query = Q(expiry__lte=datetime.now()) & Q(status__in=[2, 3])
    queryset = Images.objects.filter(query)
    print(f'delete_rejected_images(): Deleting {len(queryset)} image(s).')
    # Loop through and delete images meeting criteria
    for query in queryset:
        uploader.destroy(query.public_id)
        print(f'delete_rejected_images(): Deleted: {query.public_id}')
    # Delete expired images
    queryset.delete()
    print('delete_rejected_images(): Completed automated task.')
```

and that's it we have set up two automated tasks.

[Back to top🔝](#table-of-contents)

#### Django Crispy Forms

[Documentation for Django Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/)\

Django allows your forms to be styled using BootStrap. This provide your website forms a much more control a uniformed styling.

**Set up:**

To install in the terminal use:  `django-crispy-forms`.

At the top of any html template where you are using form fields you need to include  this tag:

```html
{% load crispy_forms_tags %}
```

Then inside your form you list each field like this

```html
{{ form.game | as_crispy_field }}
{{ form.title | as_crispy_field }}
{{ form.image | as_crispy_field }}
```

---

### JavaScript

[JavaScript website](https://www.javascript.com/)

- [JQuery](#jquery)

[Back to top🔝](#table-of-contents)

#### JQuery

[jQuery website](https://jquery.com/)

JQuery was used very significantly whenever this project needed to use JavaScript.

As the JQuery website describes it:

"**What is jQuery?**

jQuery is a fast, small, and feature-rich JavaScript library. It makes things like HTML document traversal and manipulation, event handling, animation, and Ajax much simpler with an easy-to-use API that works across a multitude of browsers. With a combination of versatility and extensibility, jQuery has changed the way that millions of people write JavaScript."

**Set up:**

To use the JQuery framework there are a few different ways, they way I did it was using a CDN.

At the bottom of the `base.html` I included this CDN script:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.3/jquery.min.js"
    integrity="sha512-STof4xm1wgkfm7heWqFJVn58Hm3EtS31XFaagaa8VMReCXAkQnJZ+jEy8PCC/iT18dFy95WcExNHFTqLyp72eQ=="
    crossorigin="anonymous" referrerpolicy="no-referrer"></script>
```

[Back to top🔝](#table-of-contents)

---

### CSS

[W3C CSS Homepage](https://www.w3.org/Style/CSS/)

[Back to top🔝](#table-of-contents)

#### BootStrap

[BootStrap website](https://getbootstrap.com/)

BootStrap is a powerful framework that mainly focuses on providing each to implement CSS with some powerful JS features such as modals.

The project was built using BootStrap 5. 99% of the styling is done using BootStrap with only little bit down in the projects own CSS file, such as colours.

There are a few ways to install BootStrap, for this project we used CDNs. We also used BootStrap icons, which is a Free, high quality, open source icon library with over 1,800 icons.

At the top of the `base.html` include these two CSS CDNs:

```html
<!-- BootStrap CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
<!-- BootStrap Icons -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css">
```

At the bottom of the `base.html` include these two JS CDNs:

```html
<!-- Popper JS -->
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"
    integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo"
    crossorigin="anonymous"></script>
<!-- BootStrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.4.1/dist/js/bootstrap.min.js"
    integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6"
    crossorigin="anonymous"></script>
```

[Back to top🔝](#table-of-contents)

---

### Widgets

- [Cloudinary](#cloudinary)
- [Select2](#select2)
- [tinyMCE](#tinymce)

[Back to top🔝](#table-of-contents)

#### Cloudinary

Cloudinary is a powerful image and video hosting service that provides services to store, transform and optimize delivery of your images to your website via an API.

For setting up Cloudinary check out the [Cloudinary Deployment](#cloudinary-deployment) section.

In Python you need to import cloudinary into your project

```py
from cloudinary import uploader
```

The way I have used Cloudinary in this project is mainly focus on uploading images and destroying images.

It was also important to bear in mind that potentially hundreds, even thousands of images could be uploaded through the website, so storage management was something to think about.

One way images could build up are as images get replaced, and the storage just being filled up with images that have been replaced. So any time an image is uploaded there is a check to see if an image already exists that is replacing and if so to destroy that image first.

```py
# If game image already exists, delete from server and replace with
# new image.
if game.image is not None and request.FILES:
    # Delete old image from Cloudinary server
    uploader.destroy(game.image.public_id)

    # Get public ID
    txt = game.image.public_id
    public_id = txt.rsplit("/", 1)[1]
    # Upload new image
    new_image = uploader.upload(
        request.FILES["image"],
        public_id=public_id,
        overwrite=True,
        folder="server_directory/"
    )
    # Save new url to game object
    game.image = new_image["url"]
```

In `forms.py` to create a field ready for Cloudinary you need to add this import:

```py
from cloudinary.forms import CloudinaryFileField
```

And then for the field in the form you can use something like:

```py
image = CloudinaryFileField(
    label="Upload new image:",
    required=False,
)
```

Finally at the top of an HTML template where you use Cloudinary to make sure you include the Cloudinary tag:

```html
{% load cloudinary %}
```

[Back to top🔝](#table-of-contents)

#### Select2

[Select2 website](https://select2.org/)

I wanted to use a dropdown widget that allowed the user to search for the correct result. As this project has the potential to have 100's of games and thousands of tags. Scrolling through those to find the one you are after could become very tedious for users, creating a bad user experience.

Fortunately I came across Select2 which as they put it "gives you a customizable select box with support for searching, tagging, remote data sets, infinite scrolling, and many other highly used options".

**Set up:**

On each HTML page where I used Select2 widget I had to include the Select2 CSS CDN in the `<head>` element.

```html
<!-- Select2 CSS CDN -->
<link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />
```

In the `<form>` section I needed to replace:

```html
{{ form.tags | as_crispy_field }}
```

with:

```html
<!-- Tag selection using Select2 -->
<label for="tags-multiple" class="mb-1">Tags:</label>
<select id="tags-multiple" class="tags-multiple" name="tags" multiple="multiple" style="width: 100%;">
    {% for tag in tags %}
    <option value="{{tag.pk}}">{{tag.name}}</option>
    {% endfor %}
</select>
```

then at the bottom of the page include Select2 JS CDN:

```html
<!-- Select2 JS CDN -->
<script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>
```

Within your own JS script you can customize the options of the Select2 widget:

```js
// DOM Ready
$(document).ready(() => {
  $('.tags-multiple').select2({
    placeholder: 'Select tags',
    allowClear: true,
    closeOnSelect: false,
  });
});
```

See the [Select2 documentation](https://select2.org/configuration/options-api) for all the JS customisable options.

[Back to top🔝](#table-of-contents)

#### tinyMCE

tinyMCE is provided by [tiny](https://www.tiny.cloud/), you can visit there website [https://www.tiny.cloud/](https://www.tiny.cloud/) and go [here for the Full Django documentation](https://django-tinymce.readthedocs.io/en/latest/)

![tinyMCE widget](./README_Images/feat_tinymce.png)

As [tiny](https://www.tiny.cloud/) put it: "TinyMCE gives you total control over your rich text editing. Either create a fully customized experience via the APIs or take advantage of the out-of-the-box enterprise-grade editor to build your next generation web app."

You will need to get an API key from [tiny](https://www.tiny.cloud/). You can find instruction on that in the [tinyMCR Deployment](#tinymce-deployment) section of this README.

In your `forms.py` you need to add the following import:

```py
from tinymce.widgets import TinyMCE
```

Then in your `forms.py`, any field you wish to have TinyMCE as the widget you just need to declare, like:

```py
short_description = forms.CharField(
    label="Short description: (min: 100, max: 200 characters)",
    min_length=100,
    max_length=200,
    widget=TinyMCE(attrs={'cols': 80, 'rows': 2}),
    required=True,
)
```

Where you plan to use tinyMCE you will need to make sure you have the tinyMCE CSS CDN in the `<head>`.

```html
<script src="https://cdn.tiny.cloud/1/r8a6ywx8flmlcce7hywu1s3qtc2dt1jyqoe1iie2vy0uwyen/tinymce/6/tinymce.min.js" referrerpolicy="origin"></script>
```

You will also need to initialise the widget on each page you use tinyMCE but putting this script at the bottom of the HTML page.

```html
<script>
    tinymce.init({
        selector: 'textarea',
        plugins: 'emoticons wordcount lists',
        menubar: false,
        statusbar: true,
        branding: true,
        elementpath: false,
        toolbar: 'wordcount | emoticons | blocks fontsize | hr | bold italic underline strikethrough | backcolor | alignleft aligncenter alignright alignjustify | indent outdent | numlist bullist| removeformat',
        content_css: "{% static 'css/tinymce.css' %}"  // resolved to http://domain.mine/mysite/mycontent.css
    });
</script>
```

If the above script you can nominate a style sheet to implement your own styling to the tinyMCE widget, as the site uses a dark background I have made the text color white

```css
body {
    color: ghostwhite;
}
```

[Back to top🔝](#table-of-contents)

---

## Testing

- [HTML](#html-testing)
- [CSS](#css-testing)
- [JavaScript](#javascript-testing)
- [Python](#python-testing) (OUTSTANDING)
  - [Linters](#python-linters)
  - [Unit Testing](#unit-testing)
  - [Coverage](#coverage)
- [User Testing](#user-testing)

### Testers

### HTML Testing

To validate all HTML, I loaded each page in a browser, I right clicked on the page, and clicked view page course (also done with keyboard shortcut CTRL+U on Chrome and Edge). I copied the code and pasted it directly in to the [W3C validator](https://validator.w3.org/nu/#textarea).

| **Page** | **Errors** | **Errors Resolved?** | **Final Result** |
| ---- | ------ | ------ | ------ |
| base | 0  | n/a | Pass |
| index | 0 | n/a | Pass |
| listings | The element button must not appear as a descendant of the a element. |  |  |
| listing | Element p not allowed as child of element span in this context. | Change `p` to `span`. | Pass |
| Terms and conditions | 0 | n/a | Pass |
| Privacy policy | 0 | n/a | Pass |
| Contact us | 0 | n/a | Pass |
| 404 | 0 | n/a | Pass |
| Login | 0 | n/a | Pass |
| Sign Up | The aria-labelledby attribute must point to an element in the same document. | Pointed to correct element. | Pass |
| Password reset | Duplicate attribute class. | Removed duplicate attr. | Pass |
| Password reset request done | 0 | n/a | Pass |
| Password reset set new password | 0 | n/a | Pass |
| Password reset completed | 0 | n/a | Pass |
| My Account | Duplicate ID modal-title. | Changed name | Pass |
|  | Duplicate ID div_id_email. | Unresolved. I was unable to find a solution using Django to change the label's id. | Error |
|  | Duplicate ID id_email. | Changed ID | Pass |
|  | Duplicate ID modal-title. | Changed name | Pass |
|  | The aria-labelledby attribute must point to an element in the same document. | Pointed to correct element | Pass |
|  | The aria-labelledby attribute must point to an element in the same document. | Pointed to correct element | Pass |
|  | The aria-labelledby attribute must point to an element in the same document. | Pointed to correct element | Pass |
| Password Change | Duplicate attribute class. | Delete duplicate attr. | Pass |
| Password Change Done | 0 | n/a | Pass |
| Server Create | Info: Trailing slash on void elements has no effect and interacts badly with unquoted attribute values. | Removed trailing slash | Pass |
| Server Edit | Info: Trailing slash on void elements has no effect and interacts badly with unquoted attribute values. | Removed trailing slash | Pass |
|  | Error: The aria-labelledby attribute must point to an element in the same document. | Pointed to correct element | Pass |
| Unauthorized | 0 | n/a | Pass |
| Sign Up - Verify email | 0 | n/a | Pass |
| Sign Up - Email verified | 0 | n/a | Pass |
| Staff account page | 0 | n/a | Pass |
| Staff - User search | Error: Stray end tag form. | Removed | Pass |
| Staff - User profile | Duplicate ID modal-title. x6 | All renamed. |  |
|  | Error: The aria-labelledby attribute must point to an element in the same document. x6 | All pointed to correct elements. | Pass |
| Staff - Game Management | Info: Trailing slash on void elements has no effect and interacts badly with unquoted attribute values. | Removed trailing slash | Pass |
|  | Warning: Empty heading. | Add placeholder text and add class 'd-none' that is removed when an appropriate action is completed. | Pass |
|  | Error: No space between attributes. | Added Space | Pass |
|  | Error: The aria-labelledby attribute must point to an element in the same document.| Pointed to element. | Pass |
| Staff - Tag Management | Info: Trailing slash on void elements has no effect and interacts badly with unquoted attribute values. | Removed trailing slash | Pass |
|  | Warning: Empty heading. | Add placeholder text and add class 'd-none' that is removed when an appropriate action is completed. | Pass |
|  | Error: The aria-labelledby attribute must point to an element in the same document. | Added Space | Pass |
| Account Delete Confirmation | 0 | n/a | Pass |
| Staff - Image Review | Error: The element button must not appear as a descendant of the a element. x2 | Change button to div | Pass |
|  | Error: The aria-labelledby attribute must point to an element in the same document. | Pointed to correct element | Pass |

### CSS Testing

As I primarily stuck with BootStrap for the styling of this project, there is not much to test for my own written CSS, but there is still a little bit, and we need to test it! For the tests we are using [W3C CSS validation Service](https://jigsaw.w3.org/css-validator/#validate_by_input).

| **File** | **Errors** | **Errors Resolved?** | **Final Result** |
| ---- | ------ | ------ | ------ |
| style.css | 0  | n/a | Pass |
| tinymce.css | 0 | n/a | Pass |

### JavaScript Testing

Testing for JavaScript was done using [ESLint](https://eslint.org/). The great thing about having [ESLint](https://eslint.org/) built into the IDE is that it shows me problems live, so I was able to fix them immediately. This has led to their be 0 problems according to [ESLint](https://eslint.org/) in my files.

| **File** | **Errors** | **Errors Resolved?** | **Final Result** |
| ---- | ------ | ------ | ------ |
| bumps | 0  | n/a | Pass |
| game_management | 0 | n/a | Pass |
| image_approval | 0 | n/a | Pass |
| my_account | 0 | n/a | Pass |
| server_create | 0 | n/a | Pass |
| server_edit | 0 | n/a | Pass |
| tag_management | 0 | n/a | Pass |
| user_management_user | 0 | n/a | Pass |
| user_management | 0 | n/a | Pass |

### Python Testing

#### Python Linters

I used 2 linters for my Python code, which were both installed on my IDE. These both provided live feedback on my code and allowed me to make sure I was always conforming to best practices.

- [PyLint](https://pylint.org/), and,
- [PyCodeStyle](https://pycodestyle.pycqa.org/en/latest/index.html) formally pep8.

[Back to top🔝](#table-of-contents)

---

## Bugs

When a bug is identified a user can raise an issue in GitHub to flag it. The user will need to complete a bug report but this helps identify the bug and know what the user expected. As I work through the project numerous of bugs would come up, but to make sure I stayed on track and focused at 1 task at a time, I raised a issue to handle the bug later.

![Bug Report ](./README_Images/feat_bug_report.png)

![Bug Report ](./README_Images/feat_bugs.png)

### Unresolved

[Link to unresolved bugs](https://github.com/BobWritesCode/server-directory-website/issues?q=is%3Aissue+is%3Aopen+label%3Abug)

### Resolved

[Link to resolved bugs](https://github.com/BobWritesCode/server-directory-website/issues?q=is%3Aissue+is%3Aclose+label%3Abug)

[Back to top🔝](#table-of-contents)

---

## Deployment

- [GitHub - Cloning](#github---cloning)
- [TinyMCE Deployment](#tinymce-deployment)
- [Cloudinary Deployment](#cloudinary-deployment)
- [ElephantSQL Deployment](#elephantsql-deployment)
- [Heroku](#heroku)

[Back to top🔝](#table-of-contents)

### GitHub - Cloning

To clone using GitHib:

Go to the project you wish to clone.

**Option 1:** If you have the [Google Chrome GitPod extension](https://chrome.google.com/webstore/detail/gitpod-always-ready-to-co/dodmmooeoklaejobgleioelladacbeki), you can just click on the Green GitPod button

:**Option 2::** Click the 'Code' button. This open options for you to clone your preferred way.

![GitHub - Cloning](./README_Images/deployment/github_cloning.png)

### TinyMCE Deployment

Go to the tiny website [https://www.tiny.cloud/](https://www.tiny.cloud/).

![tiny - ](./README_Images/deployment/tiny_1_page.png)

You will need to sign up and log in.

![tiny - ](./README_Images/deployment/tiny_2_login.png)

Part of the registration you need to put in the domain you project is being hosted, if you do not do this at registration you can go to your tiny user settings an add it later.

![tiny - ](./README_Images/deployment/tiny_3_domains.png)

On your dashboard page you will see 'Your Tiny API Key'.

![tiny - ](./README_Images/deployment/tiny_4_api.png)

### Cloudinary Deployment

**Set up:**

Go to the Cloudinary website [https://cloudinary.com/](https://cloudinary.com/).

![Cloudinary - Site](./README_Images/deployment/cloudinary_1_site.png)

You can either Log in if you have a current account or create a new account with your email address.

![Cloudinary - Log in options](./README_Images/deployment/cloudinary_2_log_in.png)

Once you have logged in or completed the registration you are taken to the main console page.

![Cloudinary - Console page](./README_Images/deployment/cloudinary_3_logged_in.png)

Click the 'Dashboard' button which is located in the nav bar.

![Cloudinary - Dashboard button](./README_Images/deployment/cloudinary_4_dashboard_button.png)

And you are now on the screen which shows you all the credential information you will require.

![Cloudinary - Dashboard page](./README_Images/deployment/cloudinary_5_dashboard.png)

### ElephantSQL Deployment

You can choose your own SQL database provider but for this project I used ElephantSQL which uses PostgresSQL databases.

**Set up:**

Go to the ElephantSQL website [https://www.elephantsql.com/](https://www.elephantsql.com/).

![ElephantSQL Front Page](./README_Images/deployment/elephantsql_1_frontpage.png)

Choose 'Log in'

![ElephantSQL Log in button](./README_Images/deployment/elephantsql_2_log_in.png)

 On the Login screen you can either log in if you have an account or you cant set up a new account.

![ElephantSQL - Log in page](./README_Images/deployment/elephantsql_3_log_in_page.png)

Their are options for you to log in / sign up with GitHub or Google, or create a new account via an email address.

![ElephantSQL - Log in options](./README_Images/deployment/elephantsql_4_log_in_options.png)

Once logged in you will see the Instances dashboard, which will be empty if you this is a new account.

![ElephantSQL - Instances dashboard](./README_Images/deployment/elephantsql_5_instances.png)

Click '+ Create New Instance'

![ElephantSQL - Create new instance](./README_Images/deployment/elephantsql_6_create_new.png)

Provide a project name of your choice.

You can choose Tiny Turtle (Free) as the plan choice.

![ElephantSQL - Select plan](./README_Images/deployment/elephantsql_7_select_plan.png)

Choose a data center near you.

![ElephantSQL - Select location](./README_Images/deployment/elephantsql_8_select_location.png)

Now just confirm what you have done is correct and click 'Create Instance'.

![ElephantSQL - Confirm](./README_Images/deployment/elephantsql_9_confirm.png)

you should now see your new instance in your dashboard, click on the 'Edit' button next to it.

![ElephantSQL - Edit](./README_Images/deployment/elephantsql_10_click_edit.png)

Here you will find the details you need to put into this project to connect it to your database.

![ElephantSQL - Credentials](./README_Images/deployment/elephantsql_11_details.png)

[Back to top🔝](#table-of-contents)

### Heroku

Navigate to your Heroku dashboard

Click "New" and select "Create new app".

![Choose new app](./README_Images/deployment/heoku-create-new-app.png)

Input a meaningful name for your app and choose the region best suited to your location.

![Heroku Region](./README_Images/deployment/heoku-app-name.png)

Select "Settings" from the tabs.

![Heroku Settings](./README_Images/deployment/heoku-settings-tab.png)

Click "Reveal Config Vars".

![Heroku Config](./README_Images/deployment/heoku-config-vars.png)

For this project you will need the following Vars:

- **CLOUDINARY_API_KEY** - Get from Cloudinary.
- **CLOUDINARY_API_SECRET** - Get from Cloudinary.
- **CLOUDINARY_CLOUD_NAME** - Get from Cloudinary.
- **CLOUDINARY_URL** - Get from Cloudinary.
- **DATABASE_URL** - Get from your SQL provider.
- **DEBUG** - Leave blank for False, any value for True.
- **DISABLE_COLLECTSTATIC** - Set to '0' (without '')
- **EMAIL_HOST** - Get from your email provider.
- **EMAIL_HOST_PASSWORD** - Get from your email provider.
- **EMAIL_HOST_USER** - Get from your email provider.
- **EMAIL_PORT** - Get from your email provider.
- **HEROKU_HOSTNAME** - Get from Heroku.
- **SECRET_KEY** - This is your Django project secret key, generated by your Django project. You can generate a new key that is different from your localhost version.
- **TINYMCE_API_KEY** - Get from TinyCloud.

![Heroku Credentials](./README_Images/deployment/heoku-input-creds.png)

Select "Deploy" from the tabs.

![Heroku Deploy](./README_Images/deployment/heroku-deploy-tab.png)

Select "GitHub - Connect to GitHub" from deployment methods.

![Heroku GitHub connect](./README_Images/deployment/heoku-select-github.png)

Click "Connect to GitHub" in the created section.

![Heroku GitHub Connect 2](./README_Images/deployment/heoku-connect-github.png)

Search for the GitHub repository by name.

Click to connect to the relevant repo.

![Heroku relevant repo](./README_Images/deployment/heoku-search-repo.png)

Either click Enable Automatic Deploys for automatic deploys or Deploy Branch to deploy manually. Manually deployed branches will need re-deploying each time the repo is updated.

![Heroku Deploy](./README_Images/deployment/heoku-branch-deploy.png)

Click View to view the deployed site.\
*Note: It may take a moment to become available.*

![Heroku View](./README_Images/deployment/heoku-view.png)

[Back to top🔝](#table-of-contents)

---

## Credits

Here is where I acknowledge contributions to this project.

- [VS Code Extensions](#vs-code-extensions)
- [Other Tech](#other-tech)
- [Content](#content)
  - [Sending email verification](#sending-email-verification)
- [Acknowledgements](#acknowledgements)

### VS Code Extensions

These are some notable VS extensions that have really helped me with this project.

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)

- [SQLite](https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite)

- [Auto Close Tag](https://open-vsx.gitpod.io/extension/formulahendry/auto-close-tag)

- [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)

- [empty-indent](https://marketplace.visualstudio.com/items?itemName=DmitryDorofeev.empty-indent)

- [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)

- [markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint)

- [indent-rainbow](https://marketplace.visualstudio.com/items?itemName=oderwat.indent-rainbow)

- [prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)

[Back to top🔝](#table-of-contents)

### Other Tech

- [Online Spellcheck](https://www.online-spellcheck.com/): To check spelling.

- [Balsamiq](https://balsamiq.com/wireframes/): To create wireframe.

- [diagrams.net](https://app.diagrams.net/): To create ERD.

- [ShareX](https://getsharex.com/): Used to snip screenshots.

[Back to top🔝](#table-of-contents)

### Content

Unless specified all code written in the .py file was my own.

Django provided the boilerplate framework for setting up the project.

#### Sending email verification

To help me get this set up, I followed this [guide](https://shafikshaon.medium.com/user-registration-with-email-verification-in-django-8aeff5ce498d).

I had to make some changes as the code in the guide did not work, which I believe was because it was created using an older person of Django.

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

### Acknowledgements

Where I have done 99% of this project by myself, my mentor **Rahul Lakhanpal** did make some design suggestions such as changing buttons with text to icons, and adding tooltips.

[Back to top🔝](#table-of-contents)

---
