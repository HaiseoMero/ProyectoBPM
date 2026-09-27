import asyncio
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from app import main, worker
from app.services import bpm_service


@pytest.mark.asyncio
async def test_worker_creates_and_closes_channel_on_running_loop(monkeypatch):
    active_loop = asyncio.get_running_loop()
    started = asyncio.Event()
    channels = []
    workers = []

    class Channel:
        def __init__(self):
            self.loop = asyncio.get_running_loop()
            self.closed = False

        async def close(self):
            self.closed = True

    class Worker:
        def __init__(self, channel, max_connection_retries):
            assert asyncio.get_running_loop() is active_loop
            assert channel.loop is active_loop
            assert max_connection_retries == -1
            self.tasks = {}
            workers.append(self)

        def task(self, task_type):
            def register(func):
                self.tasks[task_type] = func
                return func
            return register

        async def work(self):
            started.set()
            await asyncio.Event().wait()

    def make_channel(*, grpc_address):
        assert grpc_address
        channel = Channel()
        channels.append(channel)
        return channel

    monkeypatch.setattr(worker, 'create_insecure_channel', make_channel)
    monkeypatch.setattr(worker, 'ZeebeWorker', Worker)
    task = asyncio.create_task(worker.start_worker())
    await asyncio.wait_for(started.wait(), 1)
    assert set(workers[0].tasks) == {'calcular-ocean', 'generar-reporte', 'notificar-orientador'}
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert channels[0].closed is True


@pytest.mark.asyncio
async def test_lifespan_reports_worker_failure_and_closes_publisher(monkeypatch):
    async def fail_worker():
        raise RuntimeError('fallo de worker')

    async def wait_retry():
        await asyncio.Event().wait()

    close_client = AsyncMock()
    monkeypatch.setattr(main, 'init_db', AsyncMock())
    monkeypatch.setattr(main, 'start_worker', fail_worker)
    monkeypatch.setattr(main, 'retry_pending_events', wait_retry)
    monkeypatch.setattr(main, 'close_zeebe_client', close_client)
    async with main.lifespan(main.app):
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        assert main.app.state.background_errors == {'zeebe-worker': 'RuntimeError'}
        with pytest.raises(HTTPException) as error:
            await main.health_check()
        assert error.value.status_code == 503
    close_client.assert_awaited_once()


@pytest.mark.asyncio
async def test_cached_publisher_closes_and_can_reopen(monkeypatch):
    channels = []

    class Channel:
        closed = False

        async def close(self):
            self.closed = True

    def make_channel(*, grpc_address):
        assert grpc_address
        channel = Channel()
        channels.append(channel)
        return channel

    monkeypatch.setattr(bpm_service, 'create_insecure_channel', make_channel)
    monkeypatch.setattr(bpm_service, 'ZeebeClient', lambda channel: channel)
    try:
        first = bpm_service.get_zeebe_client()
        assert bpm_service.get_zeebe_client() is first
        await bpm_service.close_zeebe_client()
        assert first.closed is True
        assert bpm_service.get_zeebe_client() is not first
    finally:
        await bpm_service.close_zeebe_client()
    assert all(channel.closed for channel in channels)
