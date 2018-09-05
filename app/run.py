from app.gen import GenConsumer
from app.spot import SpotConsumer
from app.bus import Producer


def main() -> None:

    kp = Producer()
    producer = kp.connect()
    test_uri = "spotify:user:matt.kohl-gb:playlist:2d1Q2cY735lRoXC8cC6DDJ"
    kp.publish_message(producer, "playlist", "hh", test_uri)

    tasks = [
        GenConsumer("track", kp),
        SpotConsumer("playlist", kp)
    ]

    for t in tasks:
        t.start()


if __name__ == "__main__":
    main()
