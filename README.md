# jusflip
Django powered ecomm website demo. Flip through thousands of products.

## Features
- List Products
- Filter Products by category, brand and price
- Global search (backed by elasticsearch search engine)
- Responsive design

## Architecture

Uses Django python framework to open API's for product listing, filtering and search.
Product details are store on Postgres database. Bootstrap and jquery library have been used for styling and easy DOM access.
Mustache, a small templating engine has been used to dynamically render the product layout.

Global search is backed by Elasticsearch with the help of Haystack's Django ORM styled search APIs.
If Elasticsearch is down, the search fallsback to local database (postgres). 
The search results might not be relevant during fallback.
