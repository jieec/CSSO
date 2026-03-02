"""
故障树生成模块API
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    FaultTreeGenerateRequest,
    FaultTreeOptimizeRequest,
    FaultTreeData
)
from app.services.fault_tree_generator import FaultTreeGenerator

router = APIRouter()

@router.post("/generate", response_model=FaultTreeData)
async def generate_fault_tree(request: FaultTreeGenerateRequest):
    """
    生成故障树
    基于提取的知识构建层级结构
    """
    try:
        generator = FaultTreeGenerator()
        tree_data = generator.generate(
            knowledge_id=request.knowledge_id,
            top_event=request.top_event,
            max_depth=request.max_depth
        )
        return tree_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"故障树生成失败：{str(e)}")

@router.post("/optimize", response_model=FaultTreeData)
async def optimize_fault_tree(request: FaultTreeOptimizeRequest):
    """
    优化故障树
    专家修改后的逻辑校验与更新
    """
    try:
        generator = FaultTreeGenerator()
        optimized_tree = generator.optimize(
            tree_id=request.tree_id,
            modified_nodes=request.modified_nodes,
            modified_edges=request.modified_edges
        )
        return optimized_tree
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"故障树优化失败：{str(e)}")

@router.get("/{tree_id}/export")
async def export_fault_tree(tree_id: str, format: str = "json"):
    """
    导出故障树
    支持格式：json, png, svg
    """
    if format not in ["json", "png", "svg"]:
        raise HTTPException(status_code=400, detail="不支持的导出格式")
    
    # TODO: 实现导出逻辑
    return {"tree_id": tree_id, "format": format, "download_url": "/downloads/tree.json"}

@router.get("/list")
async def list_fault_trees():
    """获取故障树列表"""
    # TODO: 从数据库查询故障树列表
    return {"trees": []}
