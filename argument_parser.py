import argparse
import logging


class ArgumentParser:
    """
    Argument parser
    """

    def __init__(self) -> None:
        args_parser = argparse.ArgumentParser()
        args_parser.add_argument(
            "-br",
            "--baud_rate",
            help="COM baud rate",
            required=False,
            type=int,
            default=115200,
        )
        args_parser.add_argument(
            "-p",
            "--port",
            help="COM port",
            required=True,
            type=str,
            default="/dev/ttyUSB0",
        )
        args_parser.add_argument(
            "-ll",
            "--logger_level",
            help="Logger level info / debug",
            required=False,
            type=str,
            default="info",
            choices=["info", "debug"],
        )
        args_parser.add_argument(
            "-f",
            "--function",
            help="Function type: 0 - send frame | 1 - read buffer",
            required=True,
            type=str,
            choices=["0", "1"],
        )

        self.args = args_parser.parse_args()
        self.baud_rate = self.args.baud_rate
        self.port = self.args.port
        self.logger_level = self.args.logger_level
        self.function = self.args.function

    def get_baud_rate(self) -> int:
        return self.baud_rate

    def get_port(self) -> str:
        return self.port

    def get_logger_level(self) -> int:
        if self.logger_level == "info":
            return int(logging.INFO)
        if self.logger_level == "debug":
            return int(logging.DEBUG)

        return int(logging.INFO)

    def get_function_type(self) -> str:
        return self.function


parser = ArgumentParser()
