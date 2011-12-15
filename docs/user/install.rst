.. _install:

Installation
============

pip and easy_install
--------------------

Easiest way to install BFM is to use ``pip``:

::

    $ pip install django_bfm

And second to easiest is with ``easy_install``:

::

    $ easy_install django_bfm

However using easy_install is discouraged. Why? `Read here <http://www.pip-installer.org/en/latest/other-tools.html#pip-compared-to-easy-install>`_.

GIT repository
--------------

Alternatively, you can clone and install from Github repository, where project is developed.

::

    $ git clone git://github.com/simukis/django-bfm.git
    $ cd django-bfm
    $ python2 setup.py install

.. _configure:

Configuration
=============

Adding to Django
----------------

After downloading and installing BFM, you need to configure your Django project
to work with it.

#. Add ``'django_bfm',`` to your ``INSTALLED_APPS`` in **settings.py**,
#. Add ``url(r'^files/', include('django_bfm.urls')),`` to your ``urlpatterns`` in **urls.py**,
#. Make sure you have `staticfiles enabled <https://docs.djangoproject.com/en/dev/howto/static-files/#basic-usage>`_ (`with context processor <https://docs.djangoproject.com/en/dev/howto/static-files/#with-a-context-processor>`_) and run `python manage.py collectstatic`,
#. Make sure, that static files are served correctly by your production server.

Next steps
----------

.. toctree::
   :maxdepth: 2

   settingsvars