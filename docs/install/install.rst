Install
=======

.. highlight:: python

::
   
   pip install django-vitevue

Add to installed apps:

::

   "vv",
   
Add to the urls: 

::

   # to manage all urls with Vite Vue
   urlpatterns.append(url(r'^',include('vv.urls')))
   # or put the in your app to manage Vite Vue urls from a specific path

In the main template:

.. highlight:: django

::

   <body>
	<div id="app">
	   <!-- main template content -->
	</div>
	<script>{% block vues %}{% endblock %}</script>
   </body>
   

Load the libraries in html header:

.. highlight:: html

::

   <script type="text/javascript" src="{% static 'js/vue.min.js' %}"></script>
   <script type="text/javascript" src="{% static 'js/vuex.min.js' %}"></script>
   <script type="text/javascript" src="{% static 'js/page.js' %}"></script>
   <script type="text/javascript" src="{% static 'js/axios.min.js' %}"></script>
   <script type="text/javascript" src="{% static 'vv//vv.js' %}"></script>
   <script type="text/javascript" src="{% static 'vv/vvstore.js' %}"></script>
   