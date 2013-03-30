## isight-streamer

Publish video frames from an iSight camera to RabbitMQ.

(Non-Python) requirements:

  * Boost
  * OpenCV
  * RabbitMQ

### Installation (Mac OS X)

Download this project and install its Python dependencies:

    $ git clone git://github.com/hans/isight-streamer.git
    $ cd isight-streamer && pip install -r requirements.txt

Install Boost, OpenCV and RabbitMQ via Homebrew:

    $ brew install boost opencv rabbitmq

Open `streamer.py` and modify the constants at the top of the file if
desired. Start the RabbitMQ server if it is not already running:

    $ rabbitmq-server

Begin streaming by running `streamer.py`:

    $ python streamer.py
