import sys
import os
import json
import logging
from confluent_kafka import Consumer, Producer, KafkaError
import Ice

# Actualiza esta ruta con la ruta correcta al archivo remotetypes.ice
slice_path = os.path.join(
    os.path.dirname(__file__),
    "remotetypes",
    "remotetypes.ice",
)
Ice.loadSlice(slice_path)
import RemoteTypes as rt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KAFKA_BROKER = "localhost:9092"
REQUEST_TOPIC = "operations"
RESPONSE_TOPIC = "results"
GROUP_ID = "remotetypes_group"

def handle_message(message, factory):
    try:
        request = json.loads(message.value().decode('utf-8'))
        responses = []

        for operation in request:
            response = {"id": operation["id"]}
            try:
                object_type = getattr(rt.TypeName, operation["object_type"])
                obj = factory.get(object_type, operation["object_identifier"])
                if operation["operation"] == "iter":
                    response["status"] = "error"
                    response["error"] = "OperationNotSupported"
                else:
                    # Convert the proxy to the correct type
                    if operation["object_type"] == "RDict":
                        obj = rt.RDictPrx.checkedCast(obj)
                    elif operation["object_type"] == "RList":
                        obj = rt.RListPrx.checkedCast(obj)
                    elif operation["object_type"] == "RSet":
                        obj = rt.RSetPrx.checkedCast(obj)
                    
                    method = getattr(obj, operation["operation"])
                    args = operation.get("args", {})
                    logger.info(f"Calling method {operation['operation']} with args {args}")
                    result = method(**args)
                    response["status"] = "ok"
                    if result is not None:
                        response["result"] = result
            except Exception as e:
                logger.error(f"Error processing operation {operation}: {e}")
                response["status"] = "error"
                response["error"] = type(e).__name__
            responses.append(response)

        return json.dumps(responses).encode('utf-8')
    except Exception as e:
        logger.error(f"Failed to handle message: {e}")
        return None

def main():
    # Initialize Ice communicator
    with Ice.initialize(sys.argv) as communicator:
        proxy = communicator.stringToProxy("factory:tcp -h 127.0.0.1 -p 10000")
        factory = rt.FactoryPrx.checkedCast(proxy)
        if not factory:
            raise RuntimeError("Invalid proxy")

        # Initialize Kafka consumer
        consumer = Consumer({
            'bootstrap.servers': KAFKA_BROKER,
            'group.id': GROUP_ID,
            'auto.offset.reset': 'earliest'
        })
        consumer.subscribe([REQUEST_TOPIC])

        # Initialize Kafka producer
        producer = Producer({'bootstrap.servers': KAFKA_BROKER})

        logger.info("Client started and listening for messages...")

        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        logger.error(msg.error())
                        continue

                logger.info(f"Received message: {msg.value().decode('utf-8')}")
                response = handle_message(msg, factory)
                if response:
                    logger.info(f"Sending response: {response.decode('utf-8')}")
                    producer.produce(RESPONSE_TOPIC, response)
                    producer.flush()
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()

if __name__ == "__main__":
    main()
