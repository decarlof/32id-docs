Globus
======


All internal data transfer is handled by `Globus <https://www.globus.org>`_, if the beamline globus server is down make sure to
start the local `Globus EndPoint <https://www.globus.org/globus-connect-personal>`_ with:


Log in as usertxm@txmtwo::

	[usertxm@txmtwo]$ cd /local/Software/globusconnectpersonal-3.1.5/
	[usertxm@txmtwo]$ globusconnect