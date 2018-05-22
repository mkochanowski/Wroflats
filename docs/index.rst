.. .. image:: https://www.travis-ci.com/mkochanowski/USOSweb-automated.svg?token=mjTA3RTxEXwwcJqa4ige&branch=master
    :target: https://www.travis-ci.com/mkochanowski/wroflats

.. .. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/mkochanowski/USOSweb-automated/blob/master/LICENSE.md

.. .. image:: https://img.shields.io/badge/python-3.6-blue.svg

.. image:: https://kochanow.ski/portfolio/wroflats/mockup.png
   :scale: 50%

Can browsing real estates be a pleasurable experience? Sure!
````````````````````````````````````````````````````````````

| Let's face it - looking for a place to rent is frustrating.
| The sites with online classifieds are unintuitive and full of spam.
| And what if there is more than one person involved? Picking the right offer that all of your friends will agree on is difficult.
| 
| This app was designed to fix all of those problems.


Features
~~~~~~~~
Duplicate removal  
^^^^^^^^^^^^^^^^^

| You're tired of seeing the same flats reuploaded every single day by its owners?  
| Fear not. When you say **it's gone - it's gone**.  
| The script automatically checks for similarities between submissions and flags them as duplicates if neccessary.

Cooperative decision-making
^^^^^^^^^^^^^^^^^^^^^^^^^^^
| It has never been easier. Create a group with your friends and find a perfect place that fits all of your preferences.  
| Let your friends mark submissions as their favorites or dismiss them completely - every decision will be shared in your group, and only there.

Flexible rating
^^^^^^^^^^^^^^^
| *Apply different wages to parameters of greatest importance.*  
|   
| You're looking for a submission that has the best price-m2 ratio?  
| The fastest connection to your University by public transit?  
| Or just one that happens to have the best photos?  
  
**You decide** how the submissions are rated.

Interactive view
^^^^^^^^^^^^^^^^
| All available submissions are represented on a map with information that matters to you the most.  
| The places you and your friends marked as favorites are here.
| The places that have been removed are not.
|
| But most importantly - every submission has its price right next to it.  
| You can also individually click on every marker on the map to see more information.

Tech stack (bound to be changed while in development)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The main APIs are served using ``Flask`` with addition of the ``Flask-RESTful`` module.  
For managing asynchronous tasks such as scraping, calculating ratings or checking public transit connections, the script uses ``Celery``.  

Getting distances and public transit connections is utilized by using the ``Google Distance Matrix API``.

The resulting package is designed to be used as a docker container.  

Installation
~~~~~~~~~~~~
This project is undergoing a refactoring (basically a complete re-write) to make it more flexible and to allow for support of every city.

The documentation will soon be updated.
