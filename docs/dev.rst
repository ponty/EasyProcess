Development
=============

Tools
------------

#) setuptools_
#) Paver_
#) nose_
#) ghp-import_
#) pyflakes_
#) pychecker_
#) `paved fork`_
#) Sphinx_
#) sphinxcontrib-programscreenshot_
#) sphinxcontrib-paverutils_
#) ``autorun`` from sphinx-contrib_ 
   (there is no simple method, you have to download/unpack/setup)

Install on ubuntu
---------------------

:: 

    sudo apt-get install python-setuptools
    sudo apt-get install python-paver 
    sudo apt-get install python-nose 
    sudo easy_install ghp-import
    sudo apt-get install pyflakes 
    sudo apt-get install pychecker 
    sudo easy_install https://github.com/ponty/paved/zipball/master
    sudo apt-get install scrot
    sudo apt-get install xvfb
    sudo apt-get install xserver-xephyr
    sudo apt-get install python-imaging
    sudo apt-get install python-sphinx 
    sudo easy_install sphinxcontrib-programscreenshot
    sudo easy_install sphinxcontrib-programoutput
    sudo easy_install sphinxcontrib-paverutils
   
Tasks
-------

Paver_ is used for task management, settings are saved in pavement.py.
Sphinx_ is used to generate documentation.

print paver_ settings::

    paver printoptions    

clean generated files::

    paver clean
    
generate documentation under `docs/_build/html`::

    paver cog pdf html

upload documentation to github_::

    paver ghpages
    
run unit tests::
    
    paver nose
    #or
    nosetests --verbose
    
check python code::

    paver pyflakes 
    paver pychecker 

generate python distribution::
    
    paver sdist

upload python distribution to PyPI_::

    paver upload





.. include:: links.rst

     