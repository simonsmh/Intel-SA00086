#!/usr/bin/env python
"""
Copyright (C) 2017, Intel Corporation. All rights reserved.

String table
"""

MSG_NOT_VULNERABLE = "This system is not vulnerable." #1
MSG_VULNERABLE = "This system is vulnerable." #2
MSG_PATCHED = "This system is not vulnerable. It has already been patched." #3
MSG_RISK_ASSESSMENT = "Risk Assessment" #4
MSG_BASED = "Based on the analysis performed by this tool:" #5
MSG_EXPLANATION = "Explanation:" #6
MSG_EXPLANATION_LONG = """The detected version of the %s firmware
  is considered vulnerable for INTEL-SA-00086.
  Contact your system manufacturer for support and remediation of this system.""" #7
MSG_APP_NAME = "INTEL-SA-00086 Detection Tool" #8
MSG_APP_VER = "Application Version:" #9
MSG_SCAN_DATE = "Scan date:" #10
MSG_SYS_INFO = "Host Computer Information" #11
MSG_NAME = "Name:" #12
MSG_MANUFACTURER = "Manufacturer:" #13
MSG_MODEL = "Model:" #14
MSG_PROC = "Processor Name:" #15
MSG_OS = "OS Version:" #16
MSG_ME_INFO = "Intel(R) ME Information" #17
MSG_ENGINE = "Engine:" #18
MSG_FW_VERSION = "Version:" #19
MSG_MAY_BE_DRIVER = """Detection Error: This system may be vulnerable,
  either the Intel(R) MEI/TXEI driver is not installed
  (available from your system manufacturer)
  or the system manufacturer does not permit access
  to the ME/TXE from the host driver.""" #20
MSG_MAY_BE = "Detection Error: This system may be vulnerable." #21
MSG_PRIV = "This tool needs elevated privileges to run." #22
MSG_FOOTER = """For more information refer to the INTEL-SA-00086 Detection Tool Guide or the
  Intel Security Advisory Intel-SA-00086 at the following link:
  https://www.intel.com/sa-00086-support""" #23
#24-30 iCLS not needed here
MSG_FW_SVN = "SVN:" #31

MSG_EXPLANATION_ENG_ME = "Intel(R) Management Engine"
MSG_EXPLANATION_ENG_TXE = "Intel(R) Trusted Execution Engine"
MSG_EXPLANATION_ENG_SPS = "Intel(R) Server Platform Services"
