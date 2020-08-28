import redis
import time


class LRUSortingTable:
    """
    LRU Cache Sorting Table implemented by Redis Sorted Set
    Sets sorted by created or updated timestamp
    """
    def __init__(self, capacity):
        self.cli = redis.Redis(
            host="localhost", port="6379", db=0, decode_responses=True
        )
        self.key = "shared_mem_server:LRUSortingTable"
        self.startTime = 0

    def now(self):
        return int(round(time.time()*1000))

    def get(self, value):
        "Reactions getting resource"
        score = self.cli.zscore(self.key, value)
        if score is None:
            return None
        else:
            score = self.now()
            self.cli.zadd(self.key, {value: score})

    def put(self, value):
        """
        Reactions of putting a resource.
        """
        score = self.now()
        self.cli.zadd(self.key, {value: score})

    def getSorted(self):
        "Get Sorted Set"
        return self.cli.zrange(
            self.key, self.startTime, self.now())

    def delete(self, value):
        "Delete the value from sorted set"
        score = self.cli.zscore(self.key, value)
        print(score)
        if score is None:
            return
        return self.cli.zrem(self.key, value)

    def clear(self):
        self.cli.delete(self.key)


if __name__ == "__main__":
    lookup_table = LRUSortingTable(100)
    key = 'video-bucket:xxx.mp4'
    lookup_table.put(key)
    sortedList = lookup_table.getSorted()
    # lookup_table.delete(sortedList[0])
    lookup_table.get(key)
    lookup_table.clear()
