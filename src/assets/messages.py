class Messages:
    LINE_BREAK = ''
    DASH_LINE = '-' * 80 + '\n'

    HEADER = '''\

          _____ ____       _____      _                 _             
         |  ___|  _ \     | ____|_  _| |_ ___ _ __  ___(_) ___  _ __  
         | |_  | |_) |____|  _| \ \/ / __/ _ \ '_ \/ __| |/ _ \| '_ \ 
         |  _| |  _ <_____| |___ >  <| ||  __/ | | \__ \ | (_) | | | |
         |_|   |_| \_\    |_____/_/\_\\__\___|_| |_|___/_|\___/|_| |_|                                           

        '''

    AVERAGE_UTILITIES_HEADER = 'Average confidences this session: \n'

    BENCHMARK_UTILITIES_HEADER = 'Benchmark results this session: \n'
    BENCHMARK_UTILITIES_CPU_HEADER = 'CPU usage'
    BENCHMARK_UTILITIES_MEMORY_HEADER = 'Memory usage'
    BENCHMARK_UTILITIES_INPUT_HANDLER_HEADER = 'Input handler'
    BENCHMARK_UTILITIES_FPS_HEADER = 'FPS'

    BENCHMARK_UTILITIES_AVERAGE = ' - average {:f}%'
    BENCHMARK_UTILITIES_PEAK = ' - peak : {:f}%'
    BENCHMARK_UTILITIES_FRAME_RATIO = ' - frame ratio : {:.0f} x {:.0f}'
    BENCHMARK_UTILITIES_SCALE_FACTOR = ' - scale factor : {:.2f}'
    BENCHMARK_UTILITIES_RECORDED_FRAMES = ' - recorded frames : {:.0f}'
    BENCHMARK_UTILITIES_DETECTION_RATIO = ' - detection ratio : {:f}%'
    BENCHMARK_UTILITIES_IDENTIFICATION_RATIO = ' - identification ratio : {:f}%'
    BENCHMARK_UTILITIES_HIGHEST_FPS = ' - highest : {:.0f}'
    BENCHMARK_UTILITIES_LOWEST_FPS = ' - lowest : {:.0f}'

    AN_CONNECTOR_CONNECTION_SUCCESSFUL = 'Successfully connected to person-update topic \n'
    AN_CONNECTOR_PAYLOAD_ERROR = 'Error while parsing JSON payload \n'
    AN_CONNECTOR_CONNECTION_CLOSED = 'Connection closed, trying to reconnect ... \n'

    INPUT_HANDLER_BENCHMARK_MODE = 'Activate benchmark mode? [y/n]'
    INPUT_HANDLER_FRAME_RESCALING = 'Activate frame rescaling (performance boosting)? [y/n]'
    INPUT_HANDLER_START = 'Watching for video input changes ... \n'
    INPUT_HANDLER_IDENTIFICATION = 'Identified {:g} - changing present state'
    INPUT_HANDLER_SAMPLE_DATA = 'Persisting sample data for {}'
    INPUT_HANDLER_CLOSE = '\n Closing input handler \n'
    INPUT_HANDLER_CROP_FRAME = 'Cropping frame from {:.0f} x {:.0f} to {:.0f} x {:.0f} \n'

    MAIN_START = 'Starting FacialRecognition-Extension ... \n'

    TRAINER_START = 'Starting training ...'
    TRAINER_FINISH = 'Training finished \n'
