# Midjourney-API

This is an API for working with the popular neural network midjourney. The API is built on FastAPI. It uses the Celery task manager and Redis message broker to support the competitiveness of multiple prompts. To communicate with midjourney itself, the discord API and the corresponding library are used. 

To use this API, you need to:
1. Create a bot and obtain a token on discord developers, granting the bot administrator rights.
2. Create a channel on discord and add your bot and the midjourney bot to it.
3. Change the value in the .env file to your own.

For local deployment and testing, you can use the command "docker compose up" in the root directory of the project. If all previous steps are done correctly, the API will start running. There is a Swagger documentation available at the address http://0.0.0.0:8000/docs#, which you can use to test my API.
