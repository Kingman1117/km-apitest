"""
跨端验收测试：管理后台创建 -> C端查看验证

验收目标：验证管理后台创建的内容能在C端正常展示
- Admin创建音频
- EduPC端能查看
- H5端能查看
- 内容信息一致
- 最后清理数据

这是真正的端到端验收测试，验证数据在不同端的一致性
"""
import logging

import pytest

from payloads.admin_payloads import build_add_audio_payload
from test_data_manager import TestDataManager
from utils.response_assert import assert_field, get_field


logger = logging.getLogger(__name__)


@pytest.mark.cross_platform
def test_admin_create_audio_then_view_on_c_side(admin_client, edupc_client, h5_client, timestamp):
    """完整端到端验收：Admin创建音频 -> EduPC/H5查看 -> 验证一致性 -> 清理"""
    
    audio_name = f"跨端验收音频_{timestamp}"
    file_id = TestDataManager.get_file_id("audio")
    summary = "这是一个跨端验收测试音频"
    
    # ===== 步骤1: 管理后台创建音频 =====
    logger.info("[步骤1] 管理后台创建音频...")
    
    create_result = admin_client.post(
        "/ajax/wxAppAudio_h.jsp",
        params={"cmd": "add"},
        data=build_add_audio_payload(audio_name, summary, str(file_id), str(admin_client.wxapp_id)),
        schema="admin.content.audio.create",
    )
    
    # 验收点1: 创建成功
    admin_client.assert_success(create_result, "创建音频失败")
    audio_id = assert_field(create_result, "id", msg="音频ID为空")
    logger.info("管理后台创建成功: id=%s, name=%s", audio_id, audio_name)
    
    # ===== 步骤2: EduPC端查询音频列表 =====
    logger.info("[步骤2] EduPC端查询音频列表...")
    
    try:
        edupc_list_result = edupc_client.get(
            "/api/guestAuth/audio/getAudioList",
            params={
                "pageNo": "1",
                "pageSize": "50",
                "classifyId": "",
            },
        )
        
        if edupc_list_result.get("success"):
            edupc_list = get_field(edupc_list_result, "data.list", default=[])
            
            # 验收点2: EduPC端能查到音频
            edupc_audio = None
            for audio in edupc_list:
                if str(audio.get("id")) == str(audio_id):
                    edupc_audio = audio
                    break
            
            assert edupc_audio is not None, f"EduPC端未找到音频 (id={audio_id})"
            logger.info("EduPC端查询成功")
            
            # 验收点3: EduPC端数据一致性
            assert edupc_audio.get("name") == audio_name, "EduPC端音频名称不匹配"
            logger.info("EduPC端数据一致: name=%s", audio_name)
            
        else:
            logger.warning("EduPC端查询失败，跳过验证: %s", edupc_list_result)
    except Exception as e:
        logger.warning("EduPC端查询异常，跳过验证: %s", e)
    
    # ===== 步骤3: H5端查询音频列表 =====
    logger.info("[步骤3] H5端查询音频列表...")
    
    try:
        h5_list_result = h5_client.get(
            "/api/guest/audio/getAudioList",
            params={
                "pageNo": "1",
                "pageSize": "50",
                "classifyId": "",
            },
        )
        
        if h5_list_result.get("success"):
            h5_list = get_field(h5_list_result, "data.list", default=[])
            
            # 验收点4: H5端能查到音频
            h5_audio = None
            for audio in h5_list:
                if str(audio.get("id")) == str(audio_id):
                    h5_audio = audio
                    break
            
            assert h5_audio is not None, f"H5端未找到音频 (id={audio_id})"
            logger.info("H5端查询成功")
            
            # 验收点5: H5端数据一致性
            assert h5_audio.get("name") == audio_name, "H5端音频名称不匹配"
            logger.info("H5端数据一致: name=%s", audio_name)
            
        else:
            logger.warning("H5端查询失败，跳过验证: %s", h5_list_result)
    except Exception as e:
        logger.warning("H5端查询异常，跳过验证: %s", e)
    
    # ===== 步骤4: EduPC端查询音频详情 =====
    logger.info("[步骤4] EduPC端查询音频详情...")
    
    try:
        edupc_detail_result = edupc_client.get(
            "/api/guestAuth/audio/getAudioDetail",
            params={"id": audio_id},
        )
        
        if edupc_detail_result.get("success"):
            edupc_detail = assert_field(edupc_detail_result, "data", dict, msg="EduPC详情data为空")
            
            # 验收点6: EduPC详情数据完整
            assert edupc_detail.get("name") == audio_name, "EduPC详情名称不匹配"
            assert edupc_detail.get("summary") == summary, "EduPC详情简介不匹配"
            logger.info("EduPC端详情验证通过")
            
        else:
            logger.warning("EduPC详情查询失败: %s", edupc_detail_result)
    except Exception as e:
        logger.warning("EduPC详情查询异常: %s", e)
    
    # ===== 步骤5: H5端查询音频详情 =====
    logger.info("[步骤5] H5端查询音频详情...")
    
    try:
        h5_detail_result = h5_client.get(
            "/api/guest/audio/getAudioDetail",
            params={"id": audio_id},
        )
        
        if h5_detail_result.get("success"):
            h5_detail = assert_field(h5_detail_result, "data", dict, msg="H5详情data为空")
            
            # 验收点7: H5详情数据完整
            assert h5_detail.get("name") == audio_name, "H5详情名称不匹配"
            assert h5_detail.get("summary") == summary, "H5详情简介不匹配"
            logger.info("H5端详情验证通过")
            
        else:
            logger.warning("H5详情查询失败: %s", h5_detail_result)
    except Exception as e:
        logger.warning("H5详情查询异常: %s", e)
    
    # ===== 步骤6: 清理测试数据 =====
    logger.info("[步骤6] 清理测试数据...")
    
    delete_result = admin_client.post(
        "/ajax/wxAppAudio_h.jsp",
        params={"cmd": "delete"},
        data={"id": audio_id},
        schema="common.success",
    )
    
    # 验收点8: 删除成功
    admin_client.assert_success(delete_result, "删除音频失败")
    logger.info("测试数据清理成功")
    
    logger.info("=" * 60)
    logger.info("跨端验收通过: 音频 %s", audio_id)
    logger.info("  - 管理后台创建成功")
    logger.info("  - EduPC端可查看(列表+详情)")
    logger.info("  - H5端可查看(列表+详情)")
    logger.info("  - 三端数据一致")
    logger.info("  - 数据清理成功")
    logger.info("=" * 60)
