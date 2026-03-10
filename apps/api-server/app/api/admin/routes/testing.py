from __future__ import annotations

from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.detection import Detection
from app.models.inference_result import InferenceResult
from app.models.inference_task import InferenceTask
from app.schemas.inference import InferenceTaskRead


router = APIRouter()


@router.get(
    "/tasks",
    response_model=list[InferenceTaskRead],
    summary="读取推理测试任务",
    description="返回推理测试任务及其样例结果，用于推理测试页面展示。",
)
def read_inference_tasks(db: Session = Depends(get_db)) -> list[InferenceTaskRead]:
    tasks = list(db.scalars(select(InferenceTask).order_by(InferenceTask.created_at.desc())).all())
    grouped_results: dict[int, list[dict[str, object]]] = defaultdict(list)
    results = list(db.scalars(select(InferenceResult).order_by(InferenceResult.created_at.desc())).all())
    detections = list(db.scalars(select(Detection).order_by(Detection.created_at.asc())).all())
    grouped_detections: dict[int, list[Detection]] = defaultdict(list)
    for detection in detections:
        grouped_detections[detection.inference_result_id].append(detection)
    for result in results:
        grouped_results[result.inference_task_id].append({**result.__dict__, "detections": grouped_detections.get(result.id, [])})
    return [InferenceTaskRead.model_validate({**task.__dict__, "results": grouped_results.get(task.id, [])}) for task in tasks]
