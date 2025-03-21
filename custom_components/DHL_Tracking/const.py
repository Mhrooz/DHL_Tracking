"""Constants for dhl_tracking."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "dhl_tracking"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"

CONF_TRACKING_NUMBER = "tracking_number"
