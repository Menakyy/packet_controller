import logging
from pymodbus.client import ModbusSerialClient

logger: logging.Logger = logging.getLogger(__name__)


class ModbusClient:
    def __init__(self, com_port: str) -> None:
        self.address = 0x90
        self.modbus_client = ModbusSerialClient(
            method="rtu",
            port=com_port,
            baudrate=115200,
            stopbits=1,
            timeout=3,
        )
        self.connect_client()

    def connect_client(self) -> None:
        status = self.modbus_client.connect()
        if status:
            logger.info("Modbus client connected")
            # First test read, because first always fails
            self.modbus_client.read_coils(0, 1, self.address)
        else:
            logger.info("Failed to connect to Modbus client")
            logger.debug(f"Status: {status}")

    def close_connection(self) -> None:
        self.modbus_client.close()
