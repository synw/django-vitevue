Handle forms
============

How to post a Django form

The template
------------

Make a form template in ``myapp/templates/myapp/mymodel_form.html``:

.. highlight:: django

:: 
   
   <form id="addmymodel" onsubmit="return false" method="post">
    {% csrf_token %}
    {{ form }}
    <button class="button" @click="postMyForm()">Save</button>
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
           
           
Note: the form can be a model form or a simple form: the ``form`` and ``field`` or ``form_class`` properties are
optional

The ``PostFormView`` can handle return data and errors in the action function:

.. highlight:: python

:: 
   
    def action(self, request, clean_data):
        data = None
        error = None
        try:
            obj = MyModel.objects.save(field1=clean_data["field1"], field2=clean_data["field2"])
            data = {"object": str(obj)}
        except:
            error = "Can not save model"
        return data, error
        
The return data and error will be sent to the frontend in response to the post action

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
