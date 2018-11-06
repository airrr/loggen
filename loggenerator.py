import os
from multiprocessing import Pool, Queue
import logwriter
from cmd2 import Cmd


class LogGenerator(Cmd):

    def __init__(self):
        super().__init__(use_ipython=False)
        self.debug = True
        self._file = "/tmp/access.log"
        self.prompt = "loggen ({}) > ".format(self._file)
        self._user_count = 10
        self._host_count = 5
        self._section_count = 5
        self._log_datetime_format = "%d/%b/%Y:%H:%M:%S %z"
        self._proc_pool = None
        self._proc_queue = Queue()
        self._running = False
        self._update_prompt()

    def do_file(self, file_path) -> None:
        if not file_path:
            LogGenerator.create_file(file_path)
        if not (os.path.isfile(file_path) and os.access(file_path, os.W_OK)):
            self.perror("Missing or inaccessible file: {}".format(file_path))
            return
        else:
            self._file = file_path
            self._update_prompt()

    def do_truncate(self, _) -> None:
        was_running = self._running
        self._stop_write()
        LogGenerator.truncate_file(self._file)
        if was_running:
            self._start_write()

    def do_rotate(self, _) -> None:
        was_running = self._running
        self._stop_write()
        rotated_file = self._file + "_next"
        if os.path.isfile(rotated_file):
            os.remove(rotated_file)
        os.rename(self._file, rotated_file)
        LogGenerator.create_file(self._file)
        if was_running:
            self._start_write()

    def do_start(self, _) -> None:
        self._start_write()

    def do_stop(self, _) -> None:
        self._stop_write()

    def do_exit(self, _) -> bool:
        return True

    def _start_write(self):
        while not self._proc_queue.empty():
            self._proc_queue.get_nowait()
        pool = Pool(1, logwriter.append_http_log, (
            self._proc_queue, self._file, self._log_datetime_format, self._host_count, self._user_count,
            self._section_count,
        ))
        self._running = True
        self._proc_pool = pool
        self._update_prompt()

    def _stop_write(self):
        self._proc_queue.put("")
        if self._proc_pool:
            self._proc_pool.close()
            self._proc_pool.join()
        self._running = False
        self._update_prompt()

    def _update_prompt(self):
        self.prompt = "{} | {} > ".format('writing' if self._running else 'idle', self._file)

    @staticmethod
    def truncate_file(file_path) -> None:
        open(file_path, "w").close()

    @staticmethod
    def create_file(file_path) -> None:
        open(file_path, 'a').close()
