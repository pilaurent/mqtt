# mqtt

This code is not working properly.

Its goal is to make a **launcher.py** start an action by publishing to **server_A**.

**server_A** is processing it then send another pub to **server_B**.

**server_B** is processing it then send back a message to **server_A**.

**server_A** will update sth in database for example.

---
Schema could be :

Launcher **->** Server_A **<->** Server_B 

---

Using **paho-mqtt==1.4.0**, open up 3 terminals, and respectively launch

* python server_A.py
* python server_B.py
* python launcher.py


1. launcher.py is publishing to **mqtt/listen/thingstodo/commands**

1. server_A.py is subscribing **mqtt/listen/thingstodo/#**.

2. When work is done, server_A is publishing to **myapi/thingstodo/new/thingstodo/commands**

3. server_B.py is subscribing to **myapi/thingstodo/new/#** and 

4. when work is done,it is publishing to **myapi/thingstodo/done/thingstodo/commands**
