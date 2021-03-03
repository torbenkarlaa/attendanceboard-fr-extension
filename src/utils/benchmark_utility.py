import time

import psutil
# noinspection PyUnresolvedReferences
from assets.messages import Messages


class BenchmarkUtility:
    current_process = psutil.Process()

    frame_width = 0
    frame_height = 0
    scale_factor = 0

    cpu_measurements = []
    memory_measurements = []

    all_frames = 0
    detected_frames = 0
    identified_frames = 0

    start = time.time()
    frames = 0
    fps = []

    def measure(self, detected, identified):
        self.cpu_measurements.append(self.current_process.cpu_percent())
        self.memory_measurements.append(self.current_process.memory_percent())
        self.all_frames += 1
        self.detected_frames += 1 if detected else 0
        self.identified_frames += 1 if identified else 0

        if int(time.time() - self.start) >= 1:
            self.fps.append(self.frames)
            self.frames = 0
            self.start = time.time()
        else:
            self.frames += 1

    def print_benchmarks(self):
        print(Messages.DASH_LINE)
        print(Messages.BENCHMARK_UTILITIES_HEADER)

        print(Messages.BENCHMARK_UTILITIES_CPU_HEADER)
        print(Messages.BENCHMARK_UTILITIES_AVERAGE.format(sum(self.cpu_measurements) / len(self.cpu_measurements)))
        print(Messages.BENCHMARK_UTILITIES_PEAK.format(max(self.cpu_measurements)))
        print(Messages.LINE_BREAK)

        print(Messages.BENCHMARK_UTILITIES_MEMORY_HEADER)
        print(
            Messages.BENCHMARK_UTILITIES_AVERAGE.format(sum(self.memory_measurements) / len(self.memory_measurements)))
        print(Messages.BENCHMARK_UTILITIES_PEAK.format(max(self.memory_measurements)))
        print(Messages.LINE_BREAK)

        print(Messages.BENCHMARK_UTILITIES_INPUT_HANDLER_HEADER)
        print(Messages.BENCHMARK_UTILITIES_FRAME_RATIO.format(self.frame_width, self.frame_height))
        print(Messages.BENCHMARK_UTILITIES_SCALE_FACTOR.format(self.scale_factor))
        print(Messages.BENCHMARK_UTILITIES_RECORDED_FRAMES.format(self.all_frames))
        print(Messages.BENCHMARK_UTILITIES_DETECTION_RATIO.format((self.detected_frames / self.all_frames) * 100))
        print(Messages.BENCHMARK_UTILITIES_IDENTIFICATION_RATIO.format(
            (self.identified_frames / self.detected_frames) * 100))
        print(Messages.LINE_BREAK)

        self.fps = [i for i in self.fps if i != 0]

        print(Messages.BENCHMARK_UTILITIES_FPS_HEADER)
        print(Messages.BENCHMARK_UTILITIES_AVERAGE.format(sum(self.fps) / len(self.fps)))
        print(Messages.BENCHMARK_UTILITIES_HIGHEST_FPS.format(max(self.fps)))
        print(Messages.BENCHMARK_UTILITIES_LOWEST_FPS.format(min(self.fps)))
        print(Messages.LINE_BREAK)
