import asyncio
import websockets
import threading

async def client():
    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as websocket:
        while True:
            data = await websocket.recv()
            print(f"< {data}")

def run_client():
    asyncio.new_event_loop().run_until_complete(client())

# threads = []
# for i in range(5):  # 5개의 스레드를 생성
#     t = threading.Thread(target=run_client)
#     t.start()
#     threads.append(t)

thread = threading.Thread(target=run_client)
thread.start()
thread.join()

print(1)
# # 모든 스레드가 완료될 때까지 기다림
# for t in threads:
#     t.join()
