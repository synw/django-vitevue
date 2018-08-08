Form example
============

Example for how to post a Django form. 

The template
------------

Make a form template in `myapp/templates/myapp/mymodel_form.html`:

.. highlight:: django

:: 
   
   <form id="addmymodel" onsubmit="return false" method="post">
    {% csrf_token %}
    {{ form }}
    <button class="button" onclick="javascript:app.postMyForm()">Save</button>
   </form>

The javascript
--------------

In `myapp/vues/methods.js`:

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
	var form = document.getElementById("addmymodel");
	var data = this.serializeForm(form);
	var url = "/myapp/add/";
	this.postForm(url, data, action, error, data.csrfmiddlewaretoken)
    },
   
The Django view
---------------

In `myapp/views.py`:

.. highlight:: python

:: 
   
   # -*- coding: utf-8 -*-
   import json
   from django.http import JsonResponse
   from django.utils.html import escape
   from django.views.generic.edit import CreateView
   from vv.utils import check_csrf
   from .models import MyModel


   class MyModelCreate(CreateView):
   	model = MyModel
   	fields = ['field1", "field2"]

       def post(self, request, *args, **kwargs):
           if check_csrf(request) == False:
               return JsonResponse({"error": 1})
           data = json.loads(self.request.body.decode('utf-8'))
           field1 = escape(data['field1'])
           field2 = escape(data['field2'])
           MyModel.objects.create(field1=field1,field2=field2)
           return JsonResponse({"error": 0}

The urls
--------
 
 In `myapp/urls.py`:
 
 .. highlight:: python

:: 
   
   from django.conf.urls import include, url
   from .views import MyModelCreate

   urlpatterns = [
      url(r'^add/$', MyModelCreate.as_view(), name="mymodel-create"),
   ]
