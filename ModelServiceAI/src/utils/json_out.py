

def json_output_model(result: int | None) -> dict:
    if type(result) == int:
        return {
            "status": True,
            "num": result
        }

    else:
        return {
            "status": False,
            "num": 0
        }