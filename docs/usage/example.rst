Form example
============

Example for how to post a Django form. 

The template
------------

Make a form template in ``myapp/templates/myapp/mymodel_form.html``:

.. highlight:: django

:: 
   
   <form id="addmymodel" onsubmit="return false" method="post">
    {% csrf_token %}
    {{ form }}
    <button class="button" onclick="javascript:app.postMyForm()">Save</button>
   </form>

The javascript
--------------

In ``myapp/vues/methods.js``:

.. highlight:: javascript

:: 
   
   postMyForm: function() {
	function error(err) {
		console.log(err)
	}
	function action(response) {
		console.log(response)
		if (response.data.error === 0) {
			// do something
		} else {
			// handle error
		}
	}
	var url = "/myapp/add/";
	this.postForm(url, "addmymodel", action, error)
    },
   
The Django view
---------------

In ``myapp/views.py``:

.. highlight:: python

:: 
   
   # -*- coding: utf-8 -*-
   from vv.views import PostFormView
   from .models import MyModel


   class MyModelCreate(PostFormView):
   	model = MyModel
   	fields = ['field1", "field2"]

       def action(self, request, clean_data):
           MyModel.objects.save(field1=clean_data["field1"], field2=clean_data["field2"])

The urls
--------
 
 In ``myapp/urls.py``:
 
 .. highlight:: python

:: 
   
   from django.conf.urls import include, url
   from .views import MyModelCreate

   urlpatterns = [
      url(r'^add/$', MyModelCreate.as_view(), name="mymodel-create"),
   ]
