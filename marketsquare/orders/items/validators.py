from pydantic import BaseModel, Field
from quart import current_app, redirect, request, flash
from functools import wraps


class OrderItemArg(BaseModel):
    product_id: int = Field(strict=False)
    quantity: int = Field(gt=0, lt=21, strict=False)

# validate the request body to 
def validate__order_item_req(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        request_data = await request.form
        
        fields_required = ["product_id", "quantity"]
        for field in fields_required:
            if field not in request_data or request_data[field] == "":
                await flash("{} is required".format(field))
                return redirect(request.referrer)
        try:
            OrderItemArg(**request_data)
            return await current_app.ensure_async(f)(*args, **kwargs)
        except Exception as e:
            print(e.errors()[0])
            await flash("A required field is missing or invalid")
            return redirect(request.referrer)

    return decorated
