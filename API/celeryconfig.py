broker_url = "redis://localhost:6379/0"  # Адрес Redis для очереди
result_backend = (
    "redis://localhost:6379/0"  # Адрес Redis для хранения результатов задач
)

task_routes = {
    "send_message_to_discord": "main-queue",  # Очередь для задачи send_message_to_discord
    "run_discord_bot": "main-queue",  # Очередь для задачи run_discord_bot
}

worker_prefetch_multiplier = 1  # Установите значение, соответствующее количеству одновременно обрабатываемых задач
