Available methods
=================

State management
^^^^^^^^^^^^^^^^

A basic state management mechanism is used to manage the display. Methods:

``flush()``: reset all active items

To preserve an element from beeing flushed you can pass it to the function: ``flush("item")``

``activate(["item1", "item2"])``: set active the given items

``pushActivate(["item1", "item2"])``: add the given items to active set

``isActive("item")``: return true or false, usefull for v-show

.. highlight:: django

:: 

   this.flush();
   this.activate(["myitem"]);
   

Get and post data
^^^^^^^^^^^^^^^^^

``loadData(url, action)``: loads json data and process actions on it

:: 

   function action(data) {
      # data is parsed json
      console.log(data)
   }

   this.loadData("{% url 'myurl' %}", action);
   
``loadRawData(url, action)``: loads raw data like html and process actions on it

:: 

   function action(data) {
      # data is raw html
      app.myvar = data;
   }

   this.loadRawData("{% url 'myurl' %}", action);
   
   
``postForm(url, data, action, error, csrfmiddlewaretoken)``: post a form

Note: the ``csrfmiddlewaretoken`` is optional an will be set from the session cookie if not provided

::

   function error(err) {
    console.log(err)
   }
   function action(response) {
    console.log(response)
   }
   # formdata is a json object
   this.postForm(url, formdata, action, error, myform.csrfmiddlewaretoken)


 