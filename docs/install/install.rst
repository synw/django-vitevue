Install
=======

.. highlight:: python

::
   
   cd my_project
   git clone https://github.com/synw/django-vitevue.git && mv django-vitevue/vv .

Add to installed apps:

::

   "vv",
   
Add to the bottom of urls.py:

::

   urlpatterns.append(url(r'^',include('vv.urls')))


Include a vue block in the main template:

.. highlight:: django

::

   {% block vues %}{% endblock %}
   
   
Load the libraries in html header:

.. highlight:: html

::

   <script type="text/javascript" src="{% static 'js/vue.min.js' %}"></script>
   <script type="text/javascript" src="{% static 'js/axios.min.js' %}"></script>
   <!-- routing is optional : -->
   <script type="text/javascript" src="{% static 'js/page.js' %}"></script> 