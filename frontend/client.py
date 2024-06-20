#client.py
import asyncio
import cv2
import numpy as np
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.signaling import TcpSocketSignaling, BYE
import time

class VideoFrameReceiver(VideoStreamTrack):
    def __init__(self, track):
        super().__init__()
        self.track = track

    async def recv(self):
        frame = await self.track.recv()
        return frame

async def display_frames(queue):
    while True:
        frame = await queue.get()
        if frame is None:
            break
        frame = frame.to_ndarray(format="bgr24")
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

async def run(pc, signaling, queue):
    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("message")
        def on_message(message):
            print(f"Server: {message}")
            # Dummy coordinates
            channel.send("100,100")

    @pc.on("track")
    def on_track(track):
        print("Client received track")
        receiver = VideoFrameReceiver(track)
        pc.addTrack(receiver)

        async def recv_video():
            while True:
                frame = await receiver.recv()
                await queue.put(frame)
        asyncio.create_task(recv_video())

    await signaling.connect()
    print("Client connected to signaling")

    while True:
        obj = await signaling.receive()
        if isinstance(obj, RTCSessionDescription):
            await pc.setRemoteDescription(obj)
            if obj.type == "offer":
                await pc.setLocalDescription(await pc.createAnswer())
                await signaling.send(pc.localDescription)
                print("Client sent local description")
        elif obj is BYE:
            print("Exiting")
            break
        else:
            print(obj)

if __name__ == "__main__":
    print("Starting client")
    time.sleep(5)
    signaling = TcpSocketSignaling('backend-service.default.svc.cluster.local', 8080)
    pc = RTCPeerConnection()

    frame_queue = asyncio.Queue()

    loop = asyncio.get_event_loop()
    try:
        loop.create_task(display_frames(frame_queue))
        loop.run_until_complete(run(pc, signaling, frame_queue))
    except KeyboardInterrupt:
        pass
    finally:
        frame_queue.put_nowait(None)
        loop.run_until_complete(signaling.close())
        loop.run_until_complete(pc.close())
