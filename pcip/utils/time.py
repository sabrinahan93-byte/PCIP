from datetime import datetime, timezone, timedelta


SGT = timezone(
    timedelta(hours=8)
)


def now_sgt():

    return datetime.now(
        SGT
    )


def now_sgt_str():

    return datetime.now(
        SGT
    ).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
