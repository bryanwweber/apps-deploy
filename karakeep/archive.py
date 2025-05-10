# curl -sL -H 'Accept: application/json' -H "Authorization: Bearer
# $HOARDER_API_KEY"
# 'https://hoarder.bryanwweber.com/api/v1/lists/lb9zmm33ja9i6yzr571smz4p/bookmarks?limit=100'
# | jq '.bookmarks[].id' | xargs -n1 -P12 -- hoarder bookmarks update --archive
import pathlib
import json
import httpx
import asyncio
import jmespath
from typing import TypedDict
from rich.progress import (
    Progress,
    TaskID,
    MofNCompleteColumn,
    SpinnerColumn,
    TextColumn,
)
from dataclasses import dataclass


class Response(TypedDict):
    nextCursor: str | None
    bookmarks: list[str]


@dataclass
class BookmarkCounter:
    total: int = 0
    completed: int = 0


async def get_bookmarks(
    client: httpx.AsyncClient,
    queue: asyncio.Queue,
    counter: BookmarkCounter,
    progress: Progress,
    task_id: TaskID,
    next_cursor: str | None = None,
) -> str | None:
    url = "lists/lb9zmm33ja9i6yzr571smz4p/bookmarks"
    query = {"limit": 100}
    if next_cursor:
        query["cursor"] = next_cursor
    response = await client.get(url, params=query)
    response.raise_for_status()
    next_cursor = response.json()["nextCursor"]
    bookmarks = response.json()["bookmarks"]
    ids = jmespath.search("[].id", bookmarks)
    counter.total += len(ids)
    progress.update(task_id, total=counter.total)
    for idd in ids:
        await queue.put(idd)
    return next_cursor


async def get_all_bookmarks(
    client: httpx.AsyncClient,
    queue: asyncio.Queue,
    counter: BookmarkCounter,
    progress: Progress,
    task_id: TaskID,
) -> None:
    next_cursor = await get_bookmarks(client, queue, counter, progress, task_id)
    progress.console.print(next_cursor)
    while next_cursor is not None:
        next_cursor = await get_bookmarks(
            client, queue, counter, progress, task_id, next_cursor
        )
        progress.console.print(next_cursor)
    await queue.put(None)


async def archive_bookmarks(
    client: httpx.AsyncClient,
    queue: asyncio.Queue,
    counter: BookmarkCounter,
    progress: Progress,
    task_id: TaskID,
) -> None:
    while True:
        bookmark = await queue.get()
        if bookmark is None:
            break
        url = f"bookmarks/{bookmark}"
        data = {"archived": True}
        response = await client.patch(url, json=data)
        response.raise_for_status()
        counter.completed += 1
        progress.update(task_id, completed=counter.completed)


async def main():
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer ak1_32672650e01a219e5c11_7bef3b8f2bf70d749f7d",
    }
    bookmarks: asyncio.Queue[str | None] = asyncio.Queue()
    client = httpx.AsyncClient(
        base_url="https://hoarder.bryanwweber.com/api/v1", headers=headers
    )
    counter = BookmarkCounter()
    try:
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            SpinnerColumn(),
            MofNCompleteColumn(),
        ) as progress:
            task_id = progress.add_task("[green]Archiving bookmarks...", total=0)
            await get_all_bookmarks(client, bookmarks, counter, progress, task_id)
            await asyncio.gather(
                archive_bookmarks(client, bookmarks, counter, progress, task_id),
            )
    finally:
        remaining = []
        while True:
            try:
                remaining.append(bookmarks.get_nowait())
            except asyncio.QueueEmpty:
                break
        pathlib.Path("bookmarks.json").write_text(json.dumps(remaining))

        await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
