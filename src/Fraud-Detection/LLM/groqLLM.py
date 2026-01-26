from langchain_groq import ChatGroq


AVAILABLE_GROQ_MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]

def get_groq_llm(api_key: str, model_name: str, temperature: float = 0):
    """
    Initialize and return Groq LLM instance with user-provided API key.
    
    Args:
        api_key: User's Groq API key
        model_name: Selected model from AVAILABLE_GROQ_MODELS
        temperature: Model temperature (0 = deterministic, 1 = creative)
    
    Returns:
        ChatGroq instance configured with user settings
    
    Raises:
        ValueError: If API key is missing or invalid model selected
    """
    if not api_key or api_key.strip() == "":
        raise ValueError("Groq API key is required")
    
    if model_name not in AVAILABLE_GROQ_MODELS:
        raise ValueError(f"Invalid model '{model_name}'. Choose from: {', '.join(AVAILABLE_GROQ_MODELS)}")
    
    try:
        llm = ChatGroq(api_key=api_key, model=model_name, temperature=temperature)
        return llm
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to initialize Groq LLM: {str(e)}")
 