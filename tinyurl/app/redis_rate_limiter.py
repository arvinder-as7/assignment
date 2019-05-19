import time
from typing import Any, Tuple

import redis
from redis import Redis


def get_connection(host: str = "127.0.0.1", port: str = "6379", db: int = 0) -> Redis:
    connection = redis.Redis(host=host, port=port, db=db)
    return connection


class RateLimiter:
    API_COUNT = 'api_count'

    def __init__(self, bucket_size: int = 10, window_time: int = 60, request_limit: int = 20,
                 limit_per_ip_address: int = 4):
        # window time in seconds
        self.bucket_size = bucket_size
        self.con = get_connection()
        self.window_time = window_time
        self.request_limit = request_limit
        self.limit_per_ip = limit_per_ip_address

    @staticmethod
    def get_current_time() -> int:
        return round(time.time())

    def get_bucket(self, timestamp: int) -> int:
        factor = self.window_time // self.bucket_size
        return (timestamp // factor) * factor

    def _increment_bucket(self, bucket: int, pipeline: Any, ip_address: str):
        ip_count = pipeline.hmget(ip_address, str(bucket))[0]
        total_count = pipeline.hmget(self.API_COUNT, str(bucket))[0]
        if ip_count is None:
            ip_count = 0
        if total_count is None:
            total_count = 0
        ip_count = int(ip_count)
        total_count = int(total_count)
        pipeline.multi()
        pipeline.hmset(self.API_COUNT, {str(bucket): total_count + 1})
        pipeline.expire(self.API_COUNT, self.window_time)
        pipeline.hmset(ip_address, {str(bucket): ip_count + 1})
        pipeline.expire(ip_address, self.window_time)
        pipeline.hvals(ip_address)
        pipeline.hvals(self.API_COUNT)

    def check_if_valid_request(self, ip_address: str) -> Tuple:
        all_buckets = list(map(int, self.con.hkeys(ip_address)))
        total_count_buckets = list(map(int, self.con.hkeys(self.API_COUNT)))
        current_time_stamp = self.get_current_time()
        last_possible_time_entry = current_time_stamp - self.window_time
        buckets_to_delete = list(filter(lambda x: x < last_possible_time_entry, all_buckets))
        total_count_buckets_to_delete = list(filter(lambda x: x < last_possible_time_entry, total_count_buckets))
        if buckets_to_delete:
            self.con.delete(ip_address, *buckets_to_delete)

        if total_count_buckets_to_delete:
            self.con.delete(self.API_COUNT, *total_count_buckets_to_delete)

        current_bucket = self.get_bucket(current_time_stamp)
        _, _, _, _, requests_per_ip, total_requests = self.con.transaction(
                lambda pipe: self._increment_bucket(
                        bucket=current_bucket,
                        pipeline=pipe,
                        ip_address=ip_address
                ),
                ip_address
        )
        total_request_per_ip = sum(map(int, requests_per_ip))
        total_api_request = sum(map(int, total_requests))
        return self.request_limit, self.limit_per_ip, total_api_request, total_request_per_ip


if __name__ == '__main__':
    a = RateLimiter()
    print(a.check_if_valid_request('127.0.0.1'))
    print(a.check_if_valid_request('127.0.0.2'))
    print(a.check_if_valid_request('127.0.0.3'))
    print(a.check_if_valid_request('127.0.0.4'))
    print(a.check_if_valid_request('127.0.0.1'))
