import logging
import sys
import time
from typing import List, Awaitable, Union
from pymodbus.bit_read_message import (
    ModbusResponse,
)
from argument_parser import parser
from modbus_client import ModbusClient
from logger import init
from config import Config
from compare_buffers import compare_buffers

logger: logging.Logger = logging.getLogger(__name__)


def init_logger() -> None:
    logger_level = parser.get_logger_level()
    logger_paths: List[str] = ["modbus_client", "__main__", "compare_buffers"]
    init(logger_paths, logger_level)
    logger.info("Logger initialized")


def request_send_frame_by_radio(client: ModbusClient) -> None:
    response: Union[ModbusResponse, Awaitable[ModbusResponse]] = (
        client.modbus_client.write_coil(
            Config.RADIO_REGISTER_ADDRESS, True, Config.PACKET_ADDRESS
        )
    )
    if isinstance(response, ModbusResponse):
        if response.isError():
            logger.info(f"Error: {response}")
        else:
            logger.info("Frame sended")
    else:
        logger.info("Bad modbus type frame")


def paste_buffer_in_file(data: Union[bytes, bytearray]) -> None:
    """
    Paste the buffer in buffers.txt
    """
    # Get every second value, bacause modbus sends two bytes at a time
    buffer = " ".join([f"{x:02X}" for x in data[2::2]])
    with open("buffers.txt", "r") as file:
        existing_content = file.read().strip()

    updated_content = existing_content + " " + buffer + "\n"

    with open("buffers.txt", "w") as file:
        file.write(updated_content)


def get_frame_in_hex(data: Union[bytes, bytearray]) -> None:
    """
    Get the frame in hex format
    """
    msg = "HEX: "
    msg += " ".join([f"0x{x:02X}" for x in data[2::2]])
    logger.info(f"{msg}\n")


def compare_frame() -> bool:
    """
    Compare the buffer with the expected frame
    Paste expected frame in buffers.txt
    """
    with open("expected_frame.txt", "r") as file:
        frame = file.read().strip()

    with open("buffers.txt", "a") as file:
        file.write(frame + "\n")

    return compare_buffers()


def request_get_rx_buffer(client: ModbusClient) -> None:
    """
    Get the buffer from the radio
    """
    correct_frame = 0
    while True:
        # clear buffer.txt file
        with open("buffers.txt", "w") as file:  # pylint: disable=unused-variable
            pass

        current_register_address = int(Config.FIRST_BUFFER_REGISTER_ADDRESS)
        # reading the buffer through two reads, bacause more than 120 registers
        # return error
        for amount_of_register in [120, 28]:
            time.sleep(0.2)
            response = client.modbus_client.read_input_registers(
                current_register_address,
                amount_of_register,
                Config.PACKET_ADDRESS,
            )
            if isinstance(response, ModbusResponse):
                if response.isError():
                    logger.info(f"Error: {response}")
                else:
                    logger.info(f"DEC: {response.registers}")
                    data = response.encode()
                    get_frame_in_hex(data)
                    paste_buffer_in_file(data)
            else:
                logger.info("Bad modbus type frame")

            current_register_address += amount_of_register

        status = compare_frame()
        if status:
            correct_frame += 1

        logger.info(f"Correct frame: {correct_frame}")
        user_input = input("Press 'q' to quit: ")
        if user_input.lower() == "q":
            sys.exit()


def main() -> None:
    com_port = parser.get_port()
    client = ModbusClient(com_port)
    function_type = parser.get_function_type()

    if function_type == "0":
        request_send_frame_by_radio(client)

    if function_type == "1":
        request_get_rx_buffer(client)


if __name__ == "__main__":
    init_logger()
    main()
