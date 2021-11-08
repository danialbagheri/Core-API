## Calypso Django website project 2020

DISCLAIMER: All rights of this project are reserved for Linco Care limited.

## Instructions for future developers

All passwords are saved in environment.sh type files. It is not in the repository, and if you don't have it, you should be able to find it on the live server. use `source environment.sh` to activate it.

## Production settings to apply

- update the site url in the admin panel
- add 'instagram/calypos' folder inside the media directory

### Beta 0.1

- top seller products can now be requested from the API
- product category endpoint can now be filtered with counts, top products & product types
- Added top seller filter in the dashboard
- Prettify the code editor in the front end for easier edit of the code
- changed how name of product models to products and variants, a lot easier to read. variant option_name and option_value are also changed to one field called (variant) name.
- product type filtering is now look ups the product within the category with less sensitivity with regards to the type name (\_\_icontains)

### Beta 0.2

- Install redis on server by following instructions of this link https://redis.io/topics/quickstart
- Requirements file updated
- Website address added to environment
- New model SearchQuery added
