Manage a frontend from a module
===============================

To make a module using Vuejs frontend structure your module's template folder should contain this:

.. highlight:: python

:: 
   
   vues/data.js
   vues/methods.js
   vues/computed.js
   vues/components.js
   vues/extra.js
   routes.js
   
Put your different vuejs parts at the appropriate places. 

Note: `extra.js` is just extra global javascript, the rest are Vue parts to be assembled.

Templates
^^^^^^^^^

Put a ``<script>{% block vues %}{% endblock %}</script>`` in your base template

Settings
^^^^^^^^ 

Declare your app in settings:

::
   
   VV_APPS = ["my_app"]


Your frontend parts will be merged into the main app

Client side routing
^^^^^^^^^^^^^^^^^^^

Optional routing: make a ``routes.js`` file into your module template folder and fill it with page.js routes if needed: ex:

.. highlight:: javascript

:: 

   page('/someurl/', function(ctx, next) { app.doSomething() } );
   
Delimiters
^^^^^^^^^^

The delimiters for the vue variables are set to `{!` and `!}`. Ex:

.. highlight:: javascript

:: 

   <div>{! my_variable !}</div>

