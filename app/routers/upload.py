from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.middleware.auth import require_admin
from app.config import settings
import httpx

router = APIRouter(prefix="/api/upload", tags=["upload"])

@router.post("")
async def upload_image(file: UploadFile = File(...), _=Depends(require_admin)):
    allowed = {"image/jpeg", "image/png", "image/webp"}
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, and WebP images are allowed")

    contents = await file.read()
    path = f"products/{file.filename}"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.supabase_url}/storage/v1/object/product-images/{path}",
            headers={
                "Authorization": f"Bearer {settings.supabase_service_role_key}",
                "Content-Type": file.content_type,
            },
            content=contents,
        )

    if response.status_code not in (200, 201):
        raise HTTPException(status_code=500, detail="Image upload failed")

    public_url = f"{settings.supabase_url}/storage/v1/object/public/product-images/{path}"
    return {"url": public_url}
