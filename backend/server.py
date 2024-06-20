#server.py
import asyncio
import numpy as np
import cv2
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from aiortc.contrib.signaling import TcpSocketSignaling, BYE

WIDTH = 640
HEIGHT = 480
BALL_RADIUS = 20
SPEED_X = 5
SPEED_Y = 5

class BallStreamTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self):
        super().__init__()
        self.x = BALL_RADIUS
        self.y = BALL_RADIUS
        self.speed_x = SPEED_X
        self.speed_y = SPEED_Y

    async def recv(self):
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x - BALL_RADIUS <= 0 or self.x + BALL_RADIUS >= WIDTH:
            self.speed_x = -self.speed_x
        if self.y - BALL_RADIUS <= 0 or self.y + BALL_RADIUS >= HEIGHT:
            self.speed_y = -self.speed_y

        cv2.circle(frame, (self.x, self.y), BALL_RADIUS, (0, 255, 0), -1)
        pts, _ = cv2.imencode('.jpg', frame)
        return await asyncio.sleep(0.033, pts.tobytes())

async def run(pc, signaling):
    await signaling.connect()
    print("Server connected to signaling")

    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("message")
        def on_message(message):
            print(f"Received coordinates: {message}")

    ball_stream = BallStreamTrack()
    pc.addTrack(ball_stream)
    await pc.setLocalDescription(await pc.createOffer())
    await signaling.send(pc.localDescription)
    print("Server sent local description")

    while True:
        obj = await signaling.receive()
        if isinstance(obj, RTCSessionDescription):
            await pc.setRemoteDescription(obj)
            print("Server received and set remote description")
        elif obj is BYE:
            print("Exiting")
            break

if __name__ == "__main__":
    print("Starting server")
    signaling = TcpSocketSignaling('0.0.0.0', 8080)
    pc = RTCPeerConnection()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run(pc, signaling))
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(signaling.close())
        loop.run_until_complete(pc.close())
