"""Chat API endpoints."""

from fastapi import APIRouter, Request
from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    history_length: int


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: Request, chat_req: ChatRequest):
    """Process a chat message and return the agent's response."""
    agent = request.app.state.agent
    chat_history = request.app.state.chat_history
    
    # Add user message to history
    chat_history.add_message("user", chat_req.message)
    
    # Run the agent
    result = await agent.run(chat_req.message)
    final_answer = result["final_answer"]
    
    # Add assistant response to history
    chat_history.add_message("assistant", final_answer)
    
    return ChatResponse(
        response=final_answer,
        history_length=len(chat_history)
    )