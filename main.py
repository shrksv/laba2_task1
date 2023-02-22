from fastapi import FastAPI #імпорт модуля
app = FastAPI(title="Winged phrase") #оголошення об'єкта сервера

@app.get("/") #визначення базового URL - ендпоінта
async def root(): #функція для реалізації ендпоінта (викликатиметься під час звернення)
    return {"message": "Hello World"}