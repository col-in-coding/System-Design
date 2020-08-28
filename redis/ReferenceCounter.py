import redis


class ReferenceCounter:
    """
    Reference Counter in Redis Cache
    Used to manage the resouce uses crossing multiprocess
    """
    def __init__(self):
        self.cli = redis.Redis(
            host="localhost", port="6379", db=0, decode_responses=True
        )

    def incrRef(self, key):
        "Increase the reference, if not defined it will auto be set to 0"
        return self.cli.incr(key, amount=1)

    def decrRef(self, key):
        "Decrease the reference"
        return self.cli.decr(key, amount=1)

    def readRef(self, key):
        "Read the reference count"
        return self.cli.get(key)

    def delKey(self, key):
        "Delete key"
        return self.cli.delete(key)


if __name__ == "__main__":
    counter = ReferenceCounter()
    key = 'video-bucket:xxx.mp4'
    counter.incrRef(key)
    counter.decrRef(key)
    cnt = counter.readRef(key)
    print(cnt)
    counter.delKey(key)
