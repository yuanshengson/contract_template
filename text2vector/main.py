from fastapi import FastAPI
from pydantic import BaseModel
from FlagEmbedding import FlagModel
model = FlagModel(model_name_or_path='/data/pbx/bge-m3/BGE-M3', query_instruction_for_retrieval="", use_fp16=True)
app = FastAPI()
class TextInput(BaseModel):
    text: str
@app.post("/text2vector", include_in_schema=False)
@app.post("/text2vector/")
async def text2vector(input_data: TextInput):
    embeddings_1 = model.encode(input_data.text)
    return {"result": embeddings_1.tolist()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8032)

## uvicorn main:app --host 0.0.0.0 --port 8101 --workers 2
## curl -X POST "http://192.168.10.58:8101/text2vector/" -H "Content-Type: application/json" -d "{\"text\": \"2015年1，双方当事人均未提出上诉。\"}"
## return  {"result": embeddings_1.tolist()}