CRISIS_WORDS={'intihar','ölmek','kendimi öldür','yaşamak istemiyorum'}
def is_crisis(text:str)->bool:
    t=text.lower()
    return any(w in t for w in CRISIS_WORDS)
