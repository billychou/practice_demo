#!/usr/bin/env python
# -*- coding: utf-8  -*-
import os
from os.path import dirname as d

lib_name = os.path.basename(d(d(d(__file__))))
# logging
LOG_ROOT = '.'
PROJECT_ACCESS_LOG = "access_log"
PROJECT_INFO_LOG = "trace_log"
PROJECT_ERROR_LOG = "trace_error"
PROJECT_EXCEPTION_LOG = "trace_exception"
PROJECT_BASESERVICE_LOG = "baseservice_log"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'debug_verbose': {
            'format': '[%(asctime)s] %(levelname)s:\n %(module)s:%(lineno)d %(message)s'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s:\n %(message)s'
        },
        'exception': {
            'format': '[%(asctime)s] %(levelname)s %(module)s Line:%(lineno)d:\n'
        },
        'trace_service': {
            'format': '%(message)s'
        },
    },
    'filters': {},
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'debug_verbose'
        },
        'trace_log': {
            'level': 'INFO',
            'class': lib_name + '.djangos.logger.AosLogTimedRotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, "logs/trace_log.log"),
            'formatter': 'verbose',
            'when': 'midnight',
        },
        'trace_error': {
            'level': 'ERROR',
            'class': lib_name + '.djangos.logger.AosLogTimedRotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, "logs/trace_error.log"),
            'formatter': 'verbose',
            'when': 'midnight',
        },
        'trace_exception': {
            'level': 'ERROR',
            'class': lib_name + '.djangos.logger.AosLogTimedRotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, "logs/trace_error.log"),
            'formatter': 'exception',
            'when': 'midnight',
        },
        'access_log': {
            'level': 'INFO',
            'class': lib_name + '.djangos.logger.AosLogTimedRotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, "logs/access_log.log"),
            'formatter': 'trace_service',
            'when': 'midnight',
        },
        'baseservice_log': {
            'level': 'INFO',
            'class': lib_name + '.djangos.logger.AosLogTimedRotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, "logs/baseservice_access_log.log"),
            'formatter': 'trace_service',
            'when': 'midnight',
        },
    },
    'loggers': {
        PROJECT_ACCESS_LOG: {
            'handlers': ['access_log'],
            'level': 'INFO',
        },
        PROJECT_INFO_LOG: {
            'handlers': ['trace_log'],
            'level': 'INFO',
        },
        PROJECT_ERROR_LOG: {
            'handlers': ['trace_error'],
            'level': 'ERROR',
        },
        PROJECT_EXCEPTION_LOG: {
            'handlers': ['trace_exception'],
            'level': 'ERROR',
        },
        PROJECT_BASESERVICE_LOG: {
            'handlers': ['baseservice_log'],
            'level': 'INFO',
        },
    }
}
