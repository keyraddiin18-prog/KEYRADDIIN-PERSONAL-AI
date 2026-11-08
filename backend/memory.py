from database import save_memory, get_all_memories
from database import get_connection


def remember(key, value):
    """Save information to AI memory."""

    if not key or not value:
        return False

    save_memory(
        memory_key=key.strip(),
        memory_value=value.strip()
    )

    return True


def recall_all():
    """Retrieve all saved memories."""

    return get_all_memories()


def recall(key):
    """Retrieve a specific memory."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT memory_key, memory_value
        FROM ai_memory
        WHERE memory_key = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (key,)
    )

    result = cursor.fetchone()
    connection.close()

    if result:
        return dict(result)

    return None


def forget(memory_id):
    """Delete a specific memory."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM ai_memory WHERE id = ?",
        (memory_id,)
    )

    deleted = cursor.rowcount

    connection.commit()
    connection.close()

    return deleted > 0