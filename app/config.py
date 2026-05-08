from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Admin credentials (hashed password stored here or in DB)
    admin_email: str
    admin_password_hash: str

    # Supabase Storage
    supabase_url: str
    supabase_service_role_key: str

    cors_origins: str = "http://localhost:3000,http://localhost:3001"

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
