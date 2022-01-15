# Alpha and Beta app #

Before you run alpha and beta app, please install docker and docker-compose.

### How to run Alpha and Beta app? ###

* Clone this repository
* Run `sudo docker-compose build`
* Run `sudo docker-compose up`
* Run `sudo docker-compose exec beta bash`
* Inside bash shell of beta, run:

  ```
  /app# flask db upgrade
  /app# exit
  ```
### Endpoint Alpha ###

  [http://172.17.0.1:65412/](http://172.17.0.1:65412/)
### Endpoint Beta ###

  [http://172.17.0.1:10000/](http://172.17.0.1:10000/)
