#Based on the producer-consumer problem. Obeys FIFO.

import queue,logging,threading,time,random,concurrent.futures

def Producer(queue,order):
    #Produces order based on consumers request and puts into buffer
    while not order.is_set():
        order_message = random.randint(1, 100)
        logging.info("Producer has received an order: %s", order_message)
        queue.put(order_message)
    logging.info("Producers have no more orders.")

def Consumer(queue,order):
    #Customers(consumers) order by removing from buffer
    while not order.is_set() or not queue.empty():
        order_message = queue.get()
        logging.info("Customers picking up the order: %s (number  = %d", order_message,queue.qsize())
    logging.info("Customers have no more orders.")
    logging.info("System shuts down.")

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    pipeline = queue.Queue(maxsize=10)
    order = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as execution:
        execution.submit(Producer,pipeline,order)
        execution.submit(Consumer,pipeline,order)

        #Ensures program terminates
        time.sleep(0.5)
        logging.info("Final call!")
        order.set()
