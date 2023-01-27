# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger("paddlelabel")


def cmdOutputDebugId(debug_id):
    logger.debug(f"Debug ID: {debug_id}")
    return "OK", 200
