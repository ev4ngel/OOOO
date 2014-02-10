import thread
class Common:
    HEADER={"user-agent":"Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/25.0"}
    DEBUG=True
    DBNAME="abx.db"
    NO_TOR_NAME="NO_NAME"
    NO_TOR_URL=""
    ITEM_THREAD_NUM=3
    PIC_THREAD_NUM=2
    LOCK_DB=thread.allocate_lock()
