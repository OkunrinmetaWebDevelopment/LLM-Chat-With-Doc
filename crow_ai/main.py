from typing import Optional
from pydantic import BaseModel


class Item(BaseModel):
    # Add your input parameters here
    prompt: str
    your_param: Optional[str] = None # an example optional parameter


def predict(item, run_id, logger):
    item = Item(**item)
    
    ### ADD YOUR CODE HERE

    return {"your_results_variable": results, "your_other_return": "success"} # return your results 

