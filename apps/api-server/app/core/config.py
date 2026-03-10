from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 系统基础配置。
    app_name: str = "Infrastructure Defect Platform"
    api_prefix: str = "/api"
    app_host: str = "0.0.0.0"
    app_port: int = 2048
    root_path: str = ""
    docs_enabled: bool = True
    cors_origins: list[str] = [
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5180",
        "http://127.0.0.1:5180",
    ]

    # PostgreSQL 数据库配置。
    postgres_host: str = "127.0.0.1"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "231223"
    database_name: str = "infra_defect_platform"
    database_url: str | None = None

    # 平台初始化管理员账号。
    initial_admin_username: str = "admin"
    initial_admin_password: str = "1234"

    # 鉴权配置。
    auth_secret_key: str = "infra-defect-platform-dev-secret"
    access_token_expire_minutes: int = 720

    # 项目路径配置。
    # 当前目录为 apps/api-server/app/core，parents[4] 指向仓库根目录。
    project_root: str = str(Path(__file__).resolve().parents[4])
    storage_root: str = str(Path(__file__).resolve().parents[4] / "storage")
    upload_dir: str = str(Path(__file__).resolve().parents[4] / "storage" / "uploads")
    inference_results_dir: str = str(Path(__file__).resolve().parents[4] / "storage" / "inference-results")
    reports_dir: str = str(Path(__file__).resolve().parents[4] / "storage" / "reports")
    default_model_path: str = str(
        Path(__file__).resolve().parents[4]
        / "training"
        / "tasks"
        / "crack_detection"
        / "weights"
        / "rdd_china_crack_only_v1"
        / "weights"
        / "best.pt"
    )
    test_images_dir: str = str(Path(__file__).resolve().parents[4] / "datasets" / "test_images" / "manual")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> list[str] | Any:
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return []
            if stripped.startswith("["):
                return json.loads(stripped)
            return [item.strip() for item in stripped.split(",") if item.strip()]
        return value

    @property
    def sqlalchemy_database_uri(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.database_name}"
        )


settings = Settings()
