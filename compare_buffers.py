import logging

logger: logging.Logger = logging.getLogger(__name__)


def compare_buffers() -> bool:
    with open("buffers.txt", "r") as file:
        lines = file.readlines()

    bytes_lines = [[byte for byte in line.strip().split()] for line in lines]

    if len(bytes_lines[0]) != len(bytes_lines[1]):
        logger.info("Buffers have different lengths")
        return False
    else:
        diff_count = sum(
            1 for byte1, byte2 in zip(bytes_lines[0], bytes_lines[1]) if byte1 != byte2
        )
        if diff_count > 0:
            logger.info("Different bytes:")
            for byte1, byte2 in zip(bytes_lines[0], bytes_lines[1]):
                if byte1 != byte2:
                    print(f"Actual {byte1} | Expected {byte2}")

            logger.info(f"Diff count {diff_count}")
            logger.info(f"Number of bytes {len(bytes_lines[0])}")
            return False
        else:
            logger.info("Buffers are the same")
            logger.info(f"Number of bytes {len(bytes_lines[0])}")
            return True
