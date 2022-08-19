import logging

log = logging.getLogger("PaddleLabel")


def cmdOutputDebugId(debug_id):
    log.debug(f"Debug ID {debug_id}")
    return "OK", 200
