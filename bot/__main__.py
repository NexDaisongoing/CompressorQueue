from . import *
from .devtools import *
from aiohttp import web
import asyncio

LOGS.info("Starting...")

######## Health Check ########

async def health_check(request):
    """Health check route handler"""
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
        LOGS.info("Health check server started on port 8080")

    except Exception as e:
        LOGS.info(f"Failed to start health server: {e}")

######## Connect ########

try:
    bot.start(bot_token=BOT_TOKEN)
except Exception as er:
    LOGS.info(er)

####### GENERAL CMDS ########

@bot.on(events.NewMessage(pattern="/start"))
async def _(e):
    await start(e)

@bot.on(events.NewMessage(pattern="/ping"))
async def _(e):
    await up(e)

@bot.on(events.NewMessage(pattern="/help"))
async def _(e):
    await help(e)

@bot.on(events.NewMessage(pattern="/link"))
async def _(e):
    await dl_link(e)

######## Callbacks #########

@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"stats(.*)")))
async def _(e):
    await stats(e)

@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"skip(.*)")))
async def _(e):
    await skip(e)

@bot.on(events.callbackquery.CallbackQuery(data=re.compile("ihelp")))
async def _(e):
    await ihelp(e)

@bot.on(events.callbackquery.CallbackQuery(data=re.compile("beck")))
async def _(e):
    await beck(e)

########## Direct ###########

@bot.on(events.NewMessage(pattern="/eval"))
async def _(e):
    await eval(e)

@bot.on(events.NewMessage(pattern="/bash"))
async def _(e):
    await bash(e)

@bot.on(events.NewMessage(pattern="/usage"))
async def _(e):
    await usage(e)

########## AUTO ###########

@bot.on(events.NewMessage(incoming=True))
async def _(e):
    await encod(e)

async def something():
    for i in itertools.count():
        try:
            if not WORKING and QUEUE:
                user = int(OWNER.split()[0])
                e = await bot.send_message(user, "Downloding Queue Files...")
                s = dt.now()
                try:
                    if isinstance(QUEUE[list(QUEUE.keys())[0]], str):
                        dl = await fast_download(
                            e, list(QUEUE.keys())[0], QUEUE[list(QUEUE.keys())[0]]
                        )
                    else:
                        dl, file = QUEUE[list(QUEUE.keys())[0]]
                        tt = time.time()
                        dl = "downloads/" + dl
                        with open(dl, "wb") as f:
                            ok = await download_file(
                                client=bot,
                                location=file,
                                out=f,
                                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                                    progress(
                                        d,
                                        t,
                                        e,
                                        tt,
                                        "Downloading",
                                    )
                                ),
                            )
                except Exception as r:
                    LOGS.info(r)
                    WORKING.clear()
                    QUEUE.pop(list(QUEUE.keys())[0])
                    es = dt.now()
                    kk = dl.split("/")[-1]
                    aa = kk.split(".")[-1]
                    rr = "encode"
                    bb = kk.replace(f".{aa}", " compressed.mkv")
                    out = f"{rr}/{bb}"
                    thum = "thumb.jpg"
                    dtime = ts(int((es - s).seconds) * 1000)
                    hehe = f"{out};{dl};{list(QUEUE.keys())[0]}"
                    wah = code(hehe)
                    nn = await e.edit(
                        "Compressing..",
                        buttons=[
                            [Button.inline("STATS", data=f"stats{wah}")],
                            [Button.inline("CANCEL PROCESS", data=f"skip{wah}")],
                        ],
                    )
                    cmd = FFMPEG.format(dl, out)
                    process = await asyncio.create_subprocess_shell(
                        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
                    )
                    stdout, stderr = await process.communicate()
                    er = stderr.decode()
                    try:
                        if er:
                            await e.edit(str(er) + "\n\nERROR Contact @danish_00")
                            QUEUE.pop(list(QUEUE.keys())[0])
                            os.remove(dl)
                            os.remove(out)
                            continue
                    except BaseException:
                        pass
                    ees = dt.now()
                    ttt = time.time()
                    await nn.delete()
                    nnn = await e.client.send_message(e.chat_id, "Uploading...")
                    with open(out, "rb") as f:
                        ok = await upload_file(
                            client=e.client,
                            file=f,
                            name=out,
                            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                                progress(d, t, nnn, ttt, "uploading..")
                            ),
                        )
                    fname = out.split("/")[1]
                    ds = await e.client.send_file(
                        e.chat_id,
                        file=ok,
                        force_document=True,
                        thumb=thum,
                        caption=f"{fname}",
                    )
                    await nnn.delete()
                    org = int(Path(dl).stat().st_size)
                    com = int(Path(out).stat().st_size)
                    pe = 100 - ((com / org) * 100)
                    per = str(f"{pe:.2f}") + "%"
                    eees = dt.now()
                    x = dtime
                    xx = ts(int((ees - es).seconds) * 1000)
                    xxx = ts(int((eees - ees).seconds) * 1000)
                    a1 = await info(dl, e)
                    a2 = await info(out, e)
                    dk = await ds.reply(
                        f"Original Size : {hbs(org)}\nCompressed Size : {hbs(com)}\nCompressed Percentage : {per}\n\nMediainfo: Before//After\n\nDownloaded in {x}\nCompressed in {xx}\nUploaded in {xxx}",
                        link_preview=False,
                    )
                    QUEUE.pop(list(QUEUE.keys())[0])
                    os.remove(dl)
                    os.remove(out)
            else:
                await asyncio.sleep(3)
        except Exception as err:
            LOGS.info(err)

########### Start ############

async def startup():
    await start_health_server()  # Start health check server
    # Your existing startup code here

LOGS.info("Bot has started.")
with bot:
    bot.loop.run_until_complete(startup())
    bot.loop.run_until_complete(something())
    bot.loop.run_forever()