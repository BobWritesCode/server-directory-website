# SERVER DIRECTORY

## Full stack website

### Required app

#### django-apscheduler

pip install django-apscheduler

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
