"""
This is an example of using the library to change APN based on which sim card is inserted.
"""
from frankie import get_about, set_active_apn, connect

if __name__ == "__main__":
    aboutData = get_about()["data"]
    CURRENT_ICCID = aboutData["iccid"]

    TMOBILE_APN = 0
    ATT_APN = 3

    TMOBILE_ICCID = "1234"
    ATT_ICCID = "5678"

    if CURRENT_ICCID == TMOBILE_ICCID:
        set_active_apn(TMOBILE_APN)
        print("apn set for TMOBILE")
    elif CURRENT_ICCID == ATT_ICCID:
        set_active_apn(ATT_APN)
        print("apn set for ATT")
    else:
        print("NO ICCID match was found")

    # connect will connect using the new apn setting
    connect()