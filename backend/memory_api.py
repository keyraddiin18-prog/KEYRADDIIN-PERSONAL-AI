from fastapi import APIRouter
from memory import remember, recall_all, forget

router = APIRouter(prefix="/api/memory", tags=["Memory"])


@router.post("/")
def add_memory(key: str, value: str):
    success = remember(key, value)
    return {"success": success}


@router.get("/")
def list_memories():
    return {"memories": recall_all()}


@router.delete("/{memory_id}")
def delete_memory(memory_id: int):
    return {"success": forget(memory_id)}