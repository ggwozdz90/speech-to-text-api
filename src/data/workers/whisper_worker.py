import multiprocessing
from threading import Lock
from typing import Optional

import whisper


class WhisperWorker:
    def __init__(self) -> None:
        self._process: Optional[multiprocessing.Process] = None
        self._processing_lock = Lock()
        self._is_processing = False
        self._pipe_parent, self._pipe_child = multiprocessing.Pipe()
        self._stop_event = multiprocessing.Event()

    def start(
        self,
        device: str,
        whisper_model_name: str,
        whisper_model_download_path: str,
    ) -> None:
        if self._process is None or not self._process.is_alive():
            self._stop_event.clear()
            self._process = multiprocessing.Process(
                target=self._run_process,
                args=(
                    device,
                    whisper_model_name,
                    whisper_model_download_path,
                    self._pipe_child,
                    self._stop_event,
                ),
            )
            self._process.start()

    def is_alive(self) -> bool:
        return self._process is not None and self._process.is_alive()

    def is_processing(self) -> bool:
        return self._is_processing

    def stop(self) -> None:
        if self._process and self._process.is_alive():
            self._stop_event.set()
            self._pipe_parent.send(("stop", None))
            self._process.join(timeout=5)

            if self._process.is_alive():
                self._process.terminate()

            self._process = None

    def transcribe(
        self,
        file_path: str,
        language: str,
    ) -> dict[str, str]:
        if not self.is_alive():
            raise RuntimeError("Worker process is not running")

        with self._processing_lock:
            self._is_processing = True

            try:
                self._pipe_parent.send(("transcribe", (file_path, language)))
                result = self._pipe_parent.recv()

                if isinstance(result, Exception):
                    raise result

                return dict[str, str](result)

            finally:
                self._is_processing = False

    @staticmethod
    def _run_process(  # type: ignore
        device: str,
        whisper_model_name: str,
        whisper_model_download_path: str,
        pipe,
        stop_event,
    ) -> None:
        model = None
        try:
            model = whisper.load_model(
                whisper_model_name,
                download_root=whisper_model_download_path,
            ).to(device)

            while not stop_event.is_set():
                if pipe.poll(timeout=1):
                    command, args = pipe.recv()

                    if command == "stop":
                        break

                    elif command == "transcribe":
                        try:
                            file_path, language = args

                            kwargs = {}
                            kwargs["language"] = language[:2]

                            if device == "cpu":
                                kwargs["fp16"] = False

                            result: dict[str, str] = model.transcribe(
                                file_path,
                                **kwargs,
                            )

                            pipe.send(result)
                        except Exception as e:
                            pipe.send(e)

        finally:
            del model
            pipe.close()
