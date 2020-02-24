from cp import poll_load
from ev import get_ENV_val


sgID = get_ENV_val("sgID")
poll_load(sgID)
