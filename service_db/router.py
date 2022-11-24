from fastapi import APIRouter, Request
from schema import MessageSchema


router = APIRouter(
    tags=['items'],
    responses={404: {"description": "Page not found"}}
)


@router.post('/send-message')
async def send_message(payload: MessageSchema, request: Request):
    request.app.pika_client.send_message(
        {"message": payload.message}
    )
    return {"status": "ok"}
