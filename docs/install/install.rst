Install
=======

.. highlight:: python

::
   
   pip install django-vitevue

Add to installed apps:

::

   "vv",
   
Add to the bottom of urls.py:

::

   urlpatterns.append(url(r'^',include('vv.urls')))


In the main template:

.. highlight:: django

::
   <body>
      <div id="app">
         ...
      </div>
      <script>{% block vues %}{% endblock %}</script>
   </body>
   
   
Load the libraries in html header:

.. highlight:: html

::

   <script type="text/javascript" src="{% static 'js/vue.min.js' %}"></script>
   <script type="text/javascript" src="{% static 'js/vuex.js' %}"></script>
   <script type="text/javascript" src="{% static 'js/page.js' %}"></script>
   <script type="text/javascript" src="{% static 'js/axios.min.js' %}"></script>
   <script type="text/javascript" src="{% static 'vv//vv.js' %}"></script>
   <script type="text/javascript" src="{% static 'vv/vvstore.js' %}"></script>
   