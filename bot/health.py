from aiohttp import web
import asyncio

# Health check route handler
async def health_check(request):
    return web.Response(text="OK", status=200)

async def start_health_server():
    """Start the health check server"""
    try:
        app = web.Application()
        app.router.add_get('/health', health_check)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 8080)
        await site.start()
        print("Health check server started on port 8080")

        # Keep running forever
        while True:
            await asyncio.sleep(3600)

    except Exception as e:
        print(f"Failed to start health server: {e}")

if __name__ == "__main__":
    asyncio.run(start_health_server())