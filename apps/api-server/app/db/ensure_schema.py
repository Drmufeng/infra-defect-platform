from __future__ import annotations

from app.db.session import engine


DDL_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS audit_logs (
        id SERIAL PRIMARY KEY,
        actor_id INTEGER,
        actor_name VARCHAR(50),
        actor_role VARCHAR(50),
        action VARCHAR(100) NOT NULL,
        target_type VARCHAR(50),
        target_id INTEGER,
        request_id VARCHAR(100),
        ip VARCHAR(50),
        user_agent TEXT,
        detail_json TEXT,
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL
    )
    """,
    "CREATE INDEX IF NOT EXISTS ix_audit_logs_id ON audit_logs (id)",
    "CREATE INDEX IF NOT EXISTS ix_audit_logs_action ON audit_logs (action)",
    """
    CREATE TABLE IF NOT EXISTS artifact_files (
        id SERIAL PRIMARY KEY,
        owner_type VARCHAR(30) NOT NULL,
        owner_id INTEGER NOT NULL,
        dataset_id INTEGER REFERENCES datasets(id),
        training_job_id INTEGER REFERENCES training_jobs(id),
        inference_task_id INTEGER REFERENCES inference_tasks(id),
        model_id INTEGER REFERENCES models(id),
        file_name VARCHAR(255) NOT NULL,
        file_path VARCHAR(512) NOT NULL,
        file_type VARCHAR(50),
        mime_type VARCHAR(100),
        file_size INTEGER,
        sha256 VARCHAR(64),
        remark TEXT,
        created_by VARCHAR(50),
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL
    )
    """,
    "CREATE INDEX IF NOT EXISTS ix_artifact_files_id ON artifact_files (id)",
    "CREATE INDEX IF NOT EXISTS ix_artifact_files_owner ON artifact_files (owner_type, owner_id)",
    "ALTER TABLE datasets ADD COLUMN IF NOT EXISTS run_id VARCHAR(64)",
    "ALTER TABLE datasets ADD COLUMN IF NOT EXISTS manifest_path VARCHAR(255)",
    "ALTER TABLE datasets ADD COLUMN IF NOT EXISTS created_by VARCHAR(50)",
    "ALTER TABLE datasets ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL",
    """
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_datasets_run_id') THEN
            ALTER TABLE datasets ADD CONSTRAINT uq_datasets_run_id UNIQUE (run_id);
        END IF;
    END
    $$
    """,
    "ALTER TABLE dataset_files ADD COLUMN IF NOT EXISTS file_hash VARCHAR(128)",
    "ALTER TABLE dataset_files ADD COLUMN IF NOT EXISTS file_size INTEGER",
    "ALTER TABLE dataset_files ADD COLUMN IF NOT EXISTS remark TEXT",
    "ALTER TABLE training_jobs ADD COLUMN IF NOT EXISTS run_id VARCHAR(64)",
    "ALTER TABLE training_jobs ADD COLUMN IF NOT EXISTS model_id INTEGER REFERENCES models(id)",
    "ALTER TABLE training_jobs ADD COLUMN IF NOT EXISTS manifest_path VARCHAR(255)",
    "ALTER TABLE training_jobs ADD COLUMN IF NOT EXISTS error_message TEXT",
    "ALTER TABLE training_jobs ADD COLUMN IF NOT EXISTS created_by VARCHAR(50)",
    "ALTER TABLE training_jobs ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL",
    """
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_training_jobs_run_id') THEN
            ALTER TABLE training_jobs ADD CONSTRAINT uq_training_jobs_run_id UNIQUE (run_id);
        END IF;
    END
    $$
    """,
    "ALTER TABLE models ADD COLUMN IF NOT EXISTS model_code VARCHAR(64)",
    "ALTER TABLE models ADD COLUMN IF NOT EXISTS publish_status VARCHAR(50) DEFAULT 'draft' NOT NULL",
    "ALTER TABLE models ADD COLUMN IF NOT EXISTS published_at TIMESTAMP WITHOUT TIME ZONE",
    "ALTER TABLE models ADD COLUMN IF NOT EXISTS created_by VARCHAR(50)",
    "ALTER TABLE models ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL",
    """
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_models_model_code') THEN
            ALTER TABLE models ADD CONSTRAINT uq_models_model_code UNIQUE (model_code);
        END IF;
    END
    $$
    """,
    "ALTER TABLE inference_tasks ADD COLUMN IF NOT EXISTS run_id VARCHAR(64)",
    "ALTER TABLE inference_tasks ADD COLUMN IF NOT EXISTS report_path VARCHAR(255)",
    "ALTER TABLE inference_tasks ADD COLUMN IF NOT EXISTS manifest_path VARCHAR(255)",
    "ALTER TABLE inference_tasks ADD COLUMN IF NOT EXISTS error_message TEXT",
    "ALTER TABLE inference_tasks ADD COLUMN IF NOT EXISTS created_by VARCHAR(50)",
    "ALTER TABLE inference_tasks ADD COLUMN IF NOT EXISTS started_at TIMESTAMP WITHOUT TIME ZONE",
    "ALTER TABLE inference_tasks ADD COLUMN IF NOT EXISTS finished_at TIMESTAMP WITHOUT TIME ZONE",
    "ALTER TABLE inference_tasks ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL",
    """
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_inference_tasks_run_id') THEN
            ALTER TABLE inference_tasks ADD CONSTRAINT uq_inference_tasks_run_id UNIQUE (run_id);
        END IF;
    END
    $$
    """,
    "ALTER TABLE inference_results ADD COLUMN IF NOT EXISTS latency_ms INTEGER",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'active' NOT NULL",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL",
]


def _safe_execute(connection, statement: str) -> None:
    try:
        connection.exec_driver_sql(statement)
    except Exception as exc:  # pragma: no cover
        message = str(exc).lower()
        sqlstate = getattr(getattr(exc, "orig", None), "sqlstate", None)
        if sqlstate == "42710":
            return
        if "already exists" in message or "已存在" in message:
            return
        raise


def ensure_schema() -> None:
    with engine.begin() as connection:
        for statement in DDL_STATEMENTS:
            _safe_execute(connection, statement)


if __name__ == "__main__":
    ensure_schema()
