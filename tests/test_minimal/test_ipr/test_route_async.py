import pytest

from pyroute2 import AsyncIPRoute


@pytest.mark.parametrize(
    "command,kwarg",
    [
        ("dump", {"table": 255}),
        ("show", {"table": 255}),
        ("dump", {"match": {"table": 255}}),
        ("show", {"match": {"table": 255}}),
    ],
)
@pytest.mark.asyncio
async def test_route_filter(async_ipr, command, kwarg):
    assert set(
        [
            route.get('table')
            async for route in await async_ipr.route(command, **kwarg)
        ]
    ) == set([255])


@pytest.mark.parametrize(
    "command,kwarg",
    [
        ("dump", {"table": 255, "family": 1}),
        ("show", {"table": 255, "family": 1}),
    ],
)
@pytest.mark.asyncio
async def test_route_filter_strict(command, kwarg):
    async with AsyncIPRoute(strict_check=True) as ipr:
        assert set(
            [
                route.get('table')
                async for route in await ipr.route(command, **kwarg)
            ]
        ) == set([255])


@pytest.mark.asyncio
async def test_exception_factory():
    class MyException(Exception):
        pass

    def my_exception_factory(error):
        raise MyException(f"I received {error}")

    async with AsyncIPRoute(exception_factory=my_exception_factory) as ipr:
        with pytest.raises(MyException):
            await ipr.link("get", ifname="doesnotexists")
