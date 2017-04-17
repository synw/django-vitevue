Manage a frontend from a module
===============================

To make a module using Vuejs frontend structure do a `vues` folder in your module's template folder. It should contain this:

.. highlight:: python

:: 
   
   data.js
   methods.js
   computed.js
   extra.js
   templates.html
   
Put your different vuejs parts at the appropriate places

Templates
^^^^^^^^^

Put a ``{% block vues %}{% endblock %}`` in your base template

Settings
^^^^^^^^ 

Declare your app in settings:

::
   
   VV_APPS = ["my_app"]


Your frontend parts will be merged into the main app

Client side routing
^^^^^^^^^^^^^^^^^^^

Routing: make a ``routes.js`` file into your module template folder and fill it with page.js routes if needed: ex:

.. highlight:: javascript

:: 

   page('/someurl/', function(ctx, next) { app.doSomething() } );

