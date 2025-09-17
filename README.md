# Email reading service using Taskiq queue
This service is responsible for processing requests to read emails from rented mailboxes.

To process a large number of requests, the following are used: the asynchronous queue **Taskiq** and the **NATS** broker with JS. 

Also used here redis cache for set\get result and pub-sub mechanism for listening messages from worker. 

## Stack
* Python 3.12
* FastAPI 
* SQLAlchemy 2 (cut from the example)
* PostgreSQL (cut from the example)
* Alembic (cut from the example)
* NATS (JetStream+)
* Taskiq
* Redis

## About structure

In this project you can see mail_domain_service and mail_reader_worker-example. They should run on different nodes (or at least in different containers).

Mail Domain Service is a FastAPI app that works with a db, cache, queue etc. The main task of the service is to process requests for reading rented mailboxes. To do this, the service accepts requests and publishes tasks and data in a queue. 

The processing of tasks should be handled by a separate service. **mail_reader_worker_example** was added as an example of such a service. It reads tasks from the queue, executes them, then sends the result to the redis cache and publishes it to the channel subscribed to by redis-listener from the mail_domain service.
It must be launched as a separate application in a separate container/node.

I cant show you my db structure and specific implementations of email providers.