from __future__ import annotations

import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.inference_task import InferenceTask
from app.models.model_record import ModelRecord
from app.models.system_setting import SystemSetting
from app.schemas.client_access import (
    ClientModelRead,
    ClientProfileRead,
    ClientReportCreate,
    ClientReportCreateResponse,
)
from app.services.audit_service import write_audit_log


router = APIRouter()


def _get_float_setting(db: Session, key: str, default_value: float) -> float:
    setting = db.scalar(select(SystemSetting).where(SystemSetting.setting_key == key))
    if setting is None:
        return default_value
    try:
        return float(setting.setting_value)
    except (TypeError, ValueError):
        return default_value


@router.get(
    "/profile",
    response_model=ClientProfileRead,
    summary="读取客户端接入配置",
    description="返回客户端直连模型所需的默认参数与可用模型清单。",
)
def read_client_profile(db: Session = Depends(get_db)) -> ClientProfileRead:
    models = list(
        db.scalars(
            select(ModelRecord)
            .where(ModelRecord.status == "active", ModelRecord.publish_status == "published")
            .order_by(ModelRecord.is_default.desc(), ModelRecord.created_at.desc())
        ).all()
    )
    default_model = next((item for item in models if item.is_default), models[0] if models else None)
    default_conf_threshold = _get_float_setting(db, "default_conf_threshold", 0.46)
    test_images_setting = db.scalar(select(SystemSetting).where(SystemSetting.setting_key == "test_images_dir"))
    return ClientProfileRead(
        default_conf_threshold=default_conf_threshold,
        test_images_dir=test_images_setting.setting_value if test_images_setting else "",
        default_model_id=default_model.id if default_model else None,
        models=[
            ClientModelRead(
                id=item.id,
                name=item.name,
                model_code=item.model_code,
                model_type=item.model_type,
                weight_path=item.weight_path,
                metric_summary=item.metric_summary,
                is_default=item.is_default,
                publish_status=item.publish_status,
                status=item.status,
            )
            for item in models
        ],
    )


@router.post(
    "/reports",
    response_model=ClientReportCreateResponse,
    summary="回传客户端推理报告",
    description="客户端本地推理后将结果摘要回传后台，后台保存为推理任务记录用于追踪和展示。",
)
def create_client_report(payload: ClientReportCreate, db: Session = Depends(get_db)) -> ClientReportCreateResponse:
    run_id = payload.run_id or f"client_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
    task = InferenceTask(
        run_id=run_id,
        model_id=payload.model_id,
        source_type="client",
        input_path=payload.input_path,
        output_path=payload.output_path,
        report_path=payload.report_path,
        conf_threshold=payload.conf_threshold,
        status="finished",
        summary_json=payload.summary_json
        or json.dumps({"client_name": payload.client_name, "message": "client report uploaded"}, ensure_ascii=False),
        created_by=payload.client_name,
        started_at=datetime.now(timezone.utc),
        finished_at=datetime.now(timezone.utc),
    )
    db.add(task)
    db.flush()
    write_audit_log(
        db,
        action="client.report.uploaded",
        target_type="inference_task",
        target_id=task.id,
        detail={"client_name": payload.client_name, "run_id": run_id},
    )
    db.commit()
    db.refresh(task)

    return ClientReportCreateResponse(task_id=task.id, run_id=task.run_id or "", status=task.status, created_at=task.created_at)
