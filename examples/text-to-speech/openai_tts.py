import asyncio
import logging

from livekit import rtc
from livekit.agents import JobContext, WorkerOptions, cli
from livekit.plugins import openai


async def entrypoint(job: JobContext):
    logging.info("starting tts example agent")

    tts = openai.TTS(model="tts-1", voice="nova")

    source = rtc.AudioSource(tts.sample_rate, tts.num_channels)
    track = rtc.LocalAudioTrack.create_audio_track("agent-mic", source)
    options = rtc.TrackPublishOptions()
    options.source = rtc.TrackSource.SOURCE_MICROPHONE

    await job.connect()
    await job.room.local_participant.publish_track(track, options)

    await asyncio.sleep(1)
    logging.info('Saying "Hello!"')
    async for output in tts.synthesize("Hello!"):
        await source.capture_frame(output.frame)

    await asyncio.sleep(1)
    logging.info('Saying "Goodbye."')
    async for output in tts.synthesize("Goodbye."):
        await source.capture_frame(output.frame)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
