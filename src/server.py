from typing import Dict, List

from fastapi import FastAPI

from entry import Entry

app = FastAPI()


@app.get("")
async def server():
    """
    async function be runned by uvicorn
    """
    pass


@app.get("")
async def get_entry_batch(
    entry_obj_list: List[Entry], condiation: str = ""
) -> Dict[str, List[str]]:
    """ """
    word_list = []

    return {"words": word_list}


@app.get("")
async def get_entry():
    """
    select specific entry with specific id and only can get this one
    """
    pass


@app.get("")
async def create_entry():
    pass


@app.get("")
async def update_word():
    pass


@app.get("")
async def delete_word():
    pass
