from __future__ import annotations

from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.artifact_file import ArtifactFile
from app.models.audit_log import AuditLog
from app.models.dataset import Dataset
from app.models.dataset_file import DatasetFile
from app.models.detection import Detection
from app.models.inference_result import InferenceResult
from app.models.inference_task import InferenceTask
from app.models.model_record import ModelRecord
from app.models.system_setting import SystemSetting
from app.models.training_job import TrainingJob
from app.models.training_metric import TrainingMetric
from app.models.user import User
from app.services.audit_service import write_audit_log
from app.services.auth_service import hash_password


def _upsert_artifact(
    db: Session,
    *,
    owner_type: str,
    owner_id: int,
    file_path: str,
    file_type: str,
    created_by: str,
    dataset_id: int | None = None,
    training_job_id: int | None = None,
    inference_task_id: int | None = None,
    model_id: int | None = None,
    remark: str | None = None,
) -> None:
    existing = db.scalar(
        select(ArtifactFile).where(ArtifactFile.owner_type == owner_type, ArtifactFile.owner_id == owner_id, ArtifactFile.file_path == file_path)
    )
    if existing is not None:
        return

    path = Path(file_path)
    file_name = path.name or file_path
    file_size = path.stat().st_size if path.exists() and path.is_file() else None
    db.add(
        ArtifactFile(
            owner_type=owner_type,
            owner_id=owner_id,
            dataset_id=dataset_id,
            training_job_id=training_job_id,
            inference_task_id=inference_task_id,
            model_id=model_id,
            file_name=file_name,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
            remark=remark,
            created_by=created_by,
        )
    )


def seed_default_data(db: Session) -> None:
    # 若管理员不存在则初始化默认管理员。
    admin = db.scalar(select(User).where(User.username == settings.initial_admin_username))
    if admin is None:
        admin = User(
            username=settings.initial_admin_username,
            password_hash=hash_password(settings.initial_admin_password),
            role="admin",
            status="active",
        )
        db.add(admin)
        db.flush()
    elif admin.status != "active":
        admin.status = "active"
        admin.password_hash = hash_password(settings.initial_admin_password)

    dataset = db.scalar(select(Dataset).where(Dataset.name == "rdd_china_crack_only_v1"))
    if dataset is None:
        dataset = Dataset(
            name="rdd_china_crack_only_v1",
            task_type="infrastructure_defect_detection",
            version="v1",
            source_type="China_MotorBike",
            label_strategy="crack_only",
            raw_path=str(Path(settings.project_root) / "datasets" / "raw" / "RDD2022_China_MotorBike"),
            processed_path=str(Path(settings.project_root) / "datasets" / "processed" / "rdd_china_crack_only_v1"),
            train_count=1480,
            val_count=370,
            class_names='["crack"]',
            status="active",
            remark="当前首个裂缝检测数据集版本。",
        )
        db.add(dataset)
        db.flush()

    existing_dataset_file = db.scalar(select(DatasetFile).where(DatasetFile.dataset_id == dataset.id))
    if existing_dataset_file is None:
        db.add(
            DatasetFile(
                dataset_id=dataset.id,
                file_name="China_MotorBike_000022.jpg",
                image_path=str(Path(settings.project_root) / "datasets" / "processed" / "rdd_china_crack_only_v1" / "images" / "val" / "China_MotorBike_000022.jpg"),
                label_path=str(Path(settings.project_root) / "datasets" / "processed" / "rdd_china_crack_only_v1" / "labels" / "val" / "China_MotorBike_000022.txt"),
                split="val",
            )
        )

    training_job = db.scalar(select(TrainingJob).where(TrainingJob.job_name == "rdd_china_crack_only_v1"))
    if training_job is None:
        training_job = TrainingJob(
            job_name="rdd_china_crack_only_v1",
            dataset_id=dataset.id,
            base_weight="yolov8s.pt",
            epochs=50,
            batch_size=16,
            image_size=640,
            device="RTX 4060 Laptop GPU",
            workers=4,
            patience=20,
            status="finished",
            log_path=str(
                Path(settings.project_root)
                / "training"
                / "tasks"
                / "crack_detection"
                / "reports"
                / "training_run_history.md"
            ),
            output_dir=str(
                Path(settings.project_root)
                / "training"
                / "tasks"
                / "crack_detection"
                / "weights"
                / "rdd_china_crack_only_v1"
            ),
        )
        db.add(training_job)
        db.flush()

    training_metric = db.scalar(select(TrainingMetric).where(TrainingMetric.training_job_id == training_job.id))
    if training_metric is None:
        db.add(
            TrainingMetric(
                training_job_id=training_job.id,
                precision=0.89085,
                recall=0.87750,
                map50=0.93065,
                map50_95=0.62526,
                box_loss=1.03451,
                cls_loss=0.7452,
                dfl_loss=1.18855,
                best_epoch=50,
                results_csv_path=str(
                    Path(settings.project_root)
                    / "training"
                    / "tasks"
                    / "crack_detection"
                    / "weights"
                    / "rdd_china_crack_only_v1"
                    / "results.csv"
                ),
            )
        )
        db.flush()

    best_model = db.scalar(select(ModelRecord).where(ModelRecord.weight_path == settings.default_model_path))
    if best_model is None:
        best_model = ModelRecord(
            model_code="crack-best-v1",
            name="best.pt",
            task_type="infrastructure_defect_detection",
            dataset_id=dataset.id,
            training_job_id=training_job.id,
            weight_path=settings.default_model_path,
            model_type="yolov8",
            publish_status="published",
            metric_summary="mAP50=0.93065, mAP50-95=0.62526, precision=0.89085, recall=0.87750",
            is_default=True,
            status="active",
            created_by=settings.initial_admin_username,
        )
        db.add(best_model)
        db.flush()
    else:
        if not best_model.model_code:
            best_model.model_code = "crack-best-v1"
        best_model.publish_status = "published"
        best_model.created_by = best_model.created_by or settings.initial_admin_username

    last_model = db.scalar(
        select(ModelRecord).where(
            ModelRecord.weight_path
            == str(
                Path(settings.project_root)
                / "training"
                / "tasks"
                / "crack_detection"
                / "weights"
                / "rdd_china_crack_only_v1"
                / "weights"
                / "last.pt"
            )
        )
    )
    if last_model is None:
        db.add(
            ModelRecord(
                model_code="crack-last-v1",
                name="last.pt",
                task_type="infrastructure_defect_detection",
                dataset_id=dataset.id,
                training_job_id=training_job.id,
                weight_path=str(
                    Path(settings.project_root)
                    / "training"
                    / "tasks"
                    / "crack_detection"
                    / "weights"
                    / "rdd_china_crack_only_v1"
                    / "weights"
                    / "last.pt"
                ),
                model_type="yolov8",
                publish_status="draft",
                metric_summary="最后一轮训练模型",
                is_default=False,
                status="active",
                created_by=settings.initial_admin_username,
            )
        )
        db.flush()

    inference_task = db.scalar(select(InferenceTask).where(InferenceTask.input_path == settings.test_images_dir))
    if inference_task is None:
        inference_task = InferenceTask(
            model_id=best_model.id,
            source_type="manual",
            input_path=settings.test_images_dir,
            output_path=str(
                Path(settings.project_root)
                / "training"
                / "tasks"
                / "crack_detection"
                / "reports"
                / "test_images_inference"
                / "predict_runs"
                / "manual_test_best"
            ),
            conf_threshold=0.46,
            status="finished",
            summary_json='{"summary": "已验证 6 张测试图，整体效果良好"}',
        )
        db.add(inference_task)
        db.flush()

    sample_names = [
        "China_MotorBike_000022.jpg",
        "China_MotorBike_000028.jpg",
        "China_MotorBike_000031.jpg",
        "China_MotorBike_000032.jpg",
        "China_MotorBike_000048.jpg",
        "China_MotorBike_000052.jpg",
    ]
    for image_name in sample_names:
        result = db.scalar(
            select(InferenceResult).where(
                InferenceResult.inference_task_id == inference_task.id,
                InferenceResult.image_name == image_name,
            )
        )
        if result is None:
            result = InferenceResult(
                inference_task_id=inference_task.id,
                image_name=image_name,
                image_path=str(Path(settings.test_images_dir) / image_name),
                result_image_path=str(
                    Path(settings.project_root)
                    / "training"
                    / "tasks"
                    / "crack_detection"
                    / "reports"
                    / "test_images_inference"
                    / "predict_runs"
                    / "manual_test_best"
                    / image_name
                ),
                detected_count=1,
                summary_json='{"status": "tested"}',
            )
            db.add(result)
            db.flush()

        existing_detection = db.scalar(select(Detection).where(Detection.inference_result_id == result.id))
        if existing_detection is None:
            db.add(
                Detection(
                    inference_result_id=result.id,
                    class_name="crack",
                    confidence=0.88,
                    x1=48.0,
                    y1=72.0,
                    x2=212.0,
                    y2=418.0,
                )
            )

    default_settings = [
        ("default_conf_threshold", "0.46", "默认推理置信度阈值"),
        ("default_model_path", settings.default_model_path, "当前默认模型权重路径"),
        ("test_images_dir", settings.test_images_dir, "独立测试图片目录"),
        ("database_name", settings.database_name, "当前平台数据库名称"),
    ]
    for key, value, description in default_settings:
        existing_setting = db.scalar(select(SystemSetting).where(SystemSetting.setting_key == key))
        if existing_setting is None:
            db.add(SystemSetting(setting_key=key, setting_value=value, description=description))

    _upsert_artifact(
        db,
        owner_type="model",
        owner_id=best_model.id,
        model_id=best_model.id,
        file_path=best_model.weight_path,
        file_type="weight",
        created_by=settings.initial_admin_username,
        remark="默认发布模型权重",
    )
    _upsert_artifact(
        db,
        owner_type="training_job",
        owner_id=training_job.id,
        training_job_id=training_job.id,
        file_path=training_job.log_path or "",
        file_type="log",
        created_by=settings.initial_admin_username,
        remark="训练日志",
    )
    _upsert_artifact(
        db,
        owner_type="training_job",
        owner_id=training_job.id,
        training_job_id=training_job.id,
        file_path=str(
            Path(settings.project_root)
            / "training"
            / "tasks"
            / "crack_detection"
            / "weights"
            / "rdd_china_crack_only_v1"
            / "results.csv"
        ),
        file_type="metric",
        created_by=settings.initial_admin_username,
        remark="训练指标 CSV",
    )

    existing_seed_log = db.scalar(
        select(AuditLog).where(AuditLog.action == "system.seed.completed", AuditLog.target_type == "dataset", AuditLog.target_id == dataset.id)
    )
    if existing_seed_log is None:
        write_audit_log(
            db,
            actor=admin,
            action="system.seed.completed",
            target_type="dataset",
            target_id=dataset.id,
            detail={"dataset": dataset.name, "model": best_model.name},
        )

    db.commit()
