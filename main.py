from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import cv2
import asyncio

app = FastAPI()

# Adicione o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


async def gen_frames ():
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True: 
        try:
            success, frame = camera.read()
            if not success:
                break
            else: 
                ret, buffer = cv2.imencode('.jpg', frame) 
                frame = buffer.tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            print('connection close')
            break

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(gen_frames(), media_type="multipart/x-mixed-replace;boundary=frame")


import uvicorn
if __name__ == '__main__': 
    uvicorn.run(app, host="127.0.0.1", port=8000)
    