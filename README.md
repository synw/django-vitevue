# Django Vite Vue

Manage a Vue.js frontend from several Django modules. Uses [Vue.js](http://vuejs.org/) for data binding
and [Page.js](https://github.com/visionmedia/page.js) for client-side routing.

## Install

Clone and add `vv` to INSTALLED_APPS

Include urls at the bottom of urls.py:

  ```python
urlpatterns.append(url(r'^',include('vv.urls')))
  ```

Add a `{% block vues %}{% endblock %}` to your base template

Templates: `<header>`:

  ```html
<script type="text/javascript" src="{% static 'js/vue.min.js' %}"></script>
  ```

## Usage

To make a module using Vuejs frontend structure do a `vues` folder in your module template folder. It should contain this:

   ```
data.js
methods.js
computed.js
extra.js
templates.html
   ```
   
Put your different vuejs parts at the appropriate places

Put a `{% block vues %}` in your base template 

Routing: make a `routes.js` file into your module template folder and fill it with page.js routes if needed: ex:

   ```javasccript
page('/someurl/', function(ctx, next) { app.doSomething() } );
   ```

Declare your app in settings:

   ```python
VV_APPS = ["my_app"]
   ```
   
Your frontend parts will be merged into the main app

## Applications

- [Vvpages](https://github.com/synw/django-vvpages): pages management
- [VVcontact](https://github.com/synw/django-vvcontact): contact form
- [VVcatalog](https://github.com/synw/django-vvcatalog): products catalog with cart

## Installer and demo

To install Vite Vue you can use the [Django Mogo](https://github.com/synw/django-mogo) installer script

