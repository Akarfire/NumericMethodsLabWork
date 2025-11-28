from dataclasses import dataclass, asdict

class Results:
    
    # Some results that are going to be sent back to the UI for display
    None
    
    # Converts results structure into a dict for sending
    def dict(self) -> dict:
        return {k: str(v) for k, v in asdict(self).items()}

