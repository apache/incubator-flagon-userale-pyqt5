.. _changelog:

Changelog
=========

1.0.2 (2016-08-01)
------------------
* The elapsed time for a drag event is being recorded in the ``dragdrop`` log.

1.0.1 (2016-07-29)
------------------

* All logs will be stored to file called userale.log (configurable).
* Users can specify which events to capture by passing in a list of event keys when instantiating UserAle.
* These are the events UserAle is tracking:

	* ``mouseup``
	* ``mousedown``
	* ``mouseover``
	* ``keypress`` (optional)
	* ``keydown`` (optional)
	* ``dragenter``
	* ``dragleave``
	* ``dragmove``
	* ``dragdrop``

1.0.0 (2016-06-24)
------------------

Initial release.