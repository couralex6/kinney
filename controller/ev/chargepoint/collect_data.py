# Copyright 2020 program was created VMware, Inc.
# SPDX-License-Identifier: Apache-2.0

from cp import poll_load
from ev import get_ENV_val


sgID = get_ENV_val("sgID")
poll_load(sgID)
