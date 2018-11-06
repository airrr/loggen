import random
from datetime import datetime
import pytz

LOG_FORMAT = "{} {} {} [{}] \"{} {} HTTP/1.0\" {} {}\n"
LOG_TIMEZONE = pytz.utc
HTTP_STATUS = [200, 202, 400, 401, 403, 404, 500, 501, 502, 503, 504]
HTTP_METHOD = ["GET", "POST", "DELETE", "PUT"]
FLUSH_SIZE = 100


def append_http_log(queue, log_file_path, date_time_format, host_count=5, user_count=10, section_count=5,
                    ) -> None:
    with open(log_file_path, "w+") as log_file:
        while queue.empty():
            host = "192.168.1." + str(random.randint(0, host_count))
            user = "user" + str(random.randint(0, user_count))
            remote_user = "remoteuser" + str(random.randint(0, user_count))
            section = "/section" + str(random.randint(0, section_count))
            timestamp = datetime.now(LOG_TIMEZONE).strftime(date_time_format)
            status = HTTP_STATUS[random.randint(0, len(HTTP_STATUS) - 1)]
            method = HTTP_METHOD[random.randint(0, len(HTTP_METHOD) - 1)]
            request_size = random.randint(0, 2000)
            log_file.write(LOG_FORMAT.format(host, remote_user, user, timestamp, method, section, status, request_size))
