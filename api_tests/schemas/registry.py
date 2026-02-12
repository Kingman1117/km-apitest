"""
Schema 注册表。
"""
from pathlib import Path
from typing import Dict


_SCHEMA_BASE_DIR = Path(__file__).resolve().parent

_SCHEMA_REGISTRY: Dict[str, str] = {
    "order.commit": "order/commit_order_response.schema.json",
    "order.detail": "order/order_detail_response.schema.json",
    "answer.add_record": "answer/add_record_response.schema.json",
    "answer.detail": "answer/answer_detail_response.schema.json",
    "admin.content.audio.create": "admin/content_audio_create_response.schema.json",
    "admin.content.video.create": "admin/content_video_create_response.schema.json",
    "admin.content.news.create": "admin/content_news_create_response.schema.json",
    "admin.content.column.create": "admin/content_column_create_response.schema.json",
    "admin.ebook.create": "admin/common_create_id_response.schema.json",
    "admin.product.create": "admin/common_create_id_response.schema.json",
    "admin.question_bank.create": "admin/common_create_id_response.schema.json",
    "admin.homework.create": "admin/common_create_id_response.schema.json",
    "admin.checkpoint.create": "admin/common_create_id_response.schema.json",
    "admin.coupon.create": "admin/common_create_id_response.schema.json",
    "admin.answer_activity.create": "admin/common_create_id_response.schema.json",
    "admin.offline_course.create": "admin/common_create_id_response.schema.json",
    "admin.form.create": "admin/common_create_id_response.schema.json",
    "admin.student.create": "admin/student_create_response.schema.json",
    "admin.book_service.create": "admin/book_service_create_response.schema.json",
    "admin.evaluation.create": "admin/common_success_response.schema.json",
    "admin.redemption_code.create": "admin/common_success_response.schema.json",
    "designer.mobile.add_page": "designer/designer_add_col_response.schema.json",
    "designer.edupc.add_column": "designer/designer_add_col_response.schema.json",
    "designer.edupc.add_module": "designer/designer_add_module_response.schema.json",
    "common.success": "admin/common_success_response.schema.json",
}


def get_schema_path(schema_name: str) -> str:
    if schema_name not in _SCHEMA_REGISTRY:
        available = ", ".join(sorted(_SCHEMA_REGISTRY.keys()))
        raise KeyError(f"未知 schema: {schema_name}，可选值: {available}")

    path = _SCHEMA_BASE_DIR / _SCHEMA_REGISTRY[schema_name]
    if not path.exists():
        raise FileNotFoundError(f"schema 文件不存在: {path}")
    return str(path)

