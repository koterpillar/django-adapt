Adapt
=====

Universal data processing that can be used in place of Django forms and Django
REST framework serializers.

Concept
-------

Adapt converts between the internal and external representations of the object.
This includes:

- Displaying an internal object on a Web page and updating it based
on the user-supplied data back from a request.
- REST API with internal objects being represented as JSON.

Adapt is built on the following principles:

- Uniformity between updating primitive types (integers, strings, etc.) and
  composite types like Django models and querysets.
- Strongly typed interfaces with no implicit conversions.

Examples
--------

Building adapters
~~~~~~~~~~~~~~~~~

.. code:: python

   # Composite object adapters are built from primitive ones
   address = adapt.Object({
       'city': adapt.string,
       'street': adapt.string,
   })

   # Validations are used to restrict the acceptable values
   email = adapt.Validate(validate_email, adapt.string)

   # Primitive and composite type adapters can be used together
   user = adapt.django.Model({
       'name': adapt.string,
       'email': email,
       'address': address,
   })

   # Lists and querysets are no different
   admin = adapt.django.QuerySet(user)

   # Adapters can be used in place of forms
   class UserUpdateView(FormView):
       form_class = adapt.django.form(user)
