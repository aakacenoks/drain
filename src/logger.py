import logging as log

log.basicConfig(
    format='[%(asctime)s] (%(threadName)-10s) %(levelname)-8s %(message)s',
    level=log.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
