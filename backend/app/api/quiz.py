from fastapi import APIRouter

router = APIRouter()

@router.post("/generate")
def generate_quiz(module_id: str):
    """
    Generate 5 dummy MCQs from module content.
    Later: use LLM or prompt templates.
    """
    quiz = [
        {
            "question": f"Sample question {i} for module {module_id}",
            "options": ["A", "B", "C", "D"],
            "answer": "A",
            "difficulty": "medium"
        } for i in range(1, 6)
    ]
    return {"module_id": module_id, "quiz": quiz}
