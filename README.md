<h1 align="center" style="display: block; font-size: 2.5em; font-weight: bold; margin-block-start: 1em; margin-block-end: 1em;">
  <br /><br /><strong>BACKEND CORE</strong>
</h1>

## Introduction[](#introduction)
Backend project for linco care brands.

---

## Prerequisites[](#prerequisites)
Before deploying the project you have to make sure that you have the following pre-requisites installed:

- Docker
- Docker Compose
- Git

---

## Configurations[](#configurations)
There are some configurations needed before starting the deployment. Most of the
configurations are saved as environment variables. To add an environment variable, you must
create a `.env` file beside the docker-compose file of the project and add the variables in that file.

### Email Service
You have to set up an email service for your brand and afterward, set the
following environment variables:

- `EMAIL_HOST`
  - The host to use for sending email.
- `EMAIL_HOST_USER`
  - Username to use for the SMTP server.
- `EMAIL_HOST_PASSWORD`
  - Password to use for the SMTP server.
- `EMAIL_PORT`
  - Port to use for the SMTP server.
- `DEFAULT_FROM_EMAIL`
  - Default email address for emails through django.
  - Emails will be sent from this address.
- `EMAIL_SUBJECT_PREFIX`
  - Email subject prefix for emails sent to admins and managers through django.
- `DJANGO_ADMINS`
  - Name and email address of the django project admins.
  - Must have the following pattern: \<name>:\<address>,\<name2>:\<address2>...
  - Admins receive code error emails.
- `DEFAULT_CUSTOMER_SERVICE_EMAIL`
  - Email address of your customer service.
- `DEFAULT_MARKETING_EMAIL`
  - Email address of your marketing team.
- `VALID_STAFF_EMAIL_DOMAINS`
  - Valid email domains for the staff of your brand.
  - In some APIs, if the given email is not in one of the given domains, the API will fail.
  - Domains should be comma separated.

### Shopify

To connect to the Shopify account related to the brand, you should set the following
environment variables:

- `SHOPIFY_SHARED_SECRET_KEY`
  - Can be found in the Shopify admin
- `SHOPIFY_PASSWORD`
  - Can be found in the Shopify admin
- `SHOPIFY_API_VERSION`
  - The version of the admin API. eg: 2023-07
  - It should usually be one of the two latest versions.
- `SHOPIFY_DOMAIN`
  - Shop domain in Shopify. eg: store-name.myshopify.com

DISCLAIMER: All rights of this project are reserved for Linco Care limited.