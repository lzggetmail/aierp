"""
智慧城市知识库 - 分类配置
======================

定义智慧类领域和智能化子系统的完整分类体系
代码和文件夹结构统一使用此配置
"""

# ============================================
# 智慧类领域（40个）
# ============================================

SMART_DOMAINS = {
    # 城市级
    "智慧城市": {"keywords": ["城市大脑", "城市智能中枢", "数字政府", "一网通办", "城市运行中心", "CIM", "智慧城市"], "subsystems": ["大数据平台", "云平台", "指挥中心"]},
    "智慧园区": {"keywords": ["园区管理", "智慧产业园", "科技园区", "智慧园区"], "subsystems": ["安防系统", "停车管理", "能耗管理"]},
    "智慧社区": {"keywords": ["社区服务", "小区管理", "智慧小区", "智慧社区"], "subsystems": ["门禁通行", "视频监控", "信息发布"]},
    "智慧建筑": {"keywords": ["智能建筑", "绿色建筑", "智慧楼宇", "智慧建筑"], "subsystems": ["楼宇自控", "照明系统", "能耗管理"]},
    
    # 行业级
    "智慧医院": {"keywords": ["智慧医疗", "医院信息化", "远程医疗", "智慧医院"], "subsystems": ["物联网平台", "大数据平台", "安防系统"]},
    "智慧学校": {"keywords": ["智慧校园", "智慧教育", "校园安防", "智慧学校"], "subsystems": ["安防系统", "广播系统", "一卡通"]},
    "智慧交通": {"keywords": ["智能交通", "交通大脑", "智慧出行", "信号控制", "电子警察", "智慧交通"], "subsystems": ["视频监控", "信息发布", "大数据平台"]},
    "智慧停车": {"keywords": ["智慧停车", "智能停车场", "停车诱导", "停车场"], "subsystems": ["停车管理", "视频监控", "门禁通行"]},
    
    # 政务级
    "智慧政务": {"keywords": ["数字政府", "一网通办", "政务大厅"], "subsystems": ["大数据平台", "云平台", "信息发布"]},
    "智慧警务": {"keywords": ["智慧公安", "警务云", "雪亮工程"], "subsystems": ["视频监控", "安防系统", "指挥中心"]},
    "智慧消防": {"keywords": ["智慧消防", "消防物联网", "火灾预警"], "subsystems": ["消防系统", "物联网平台", "指挥中心"]},
    
    # 公用事业
    "智慧环保": {"keywords": ["智慧环保", "环境监测", "污染监控"], "subsystems": ["环境监测", "物联网平台", "大数据平台"]},
    "智慧水务": {"keywords": ["智慧水务", "供水管理", "漏损监测"], "subsystems": ["给排水", "物联网平台", "大数据平台"]},
    "智慧能源": {"keywords": ["智慧能源", "能耗管理", "节能降碳"], "subsystems": ["能耗管理", "供配电", "大数据平台"]},
    "智慧电网": {"keywords": ["智能电网", "电力物联网", "配网自动化"], "subsystems": ["供配电", "物联网平台", "大数据平台"]},
    "智慧路灯": {"keywords": ["智慧路灯", "智能照明", "路灯管理"], "subsystems": ["照明系统", "物联网平台", "能耗管理"]},
    
    # 产业级
    "智慧物流": {"keywords": ["智慧物流", "智能仓储", "物流园区"], "subsystems": ["物联网平台", "数据中心", "视频监控"]},
    "智慧工厂": {"keywords": ["智慧工厂", "智能制造", "工业4.0"], "subsystems": ["物联网平台", "大数据平台", "楼宇自控"]},
    "智慧农业": {"keywords": ["智慧农业", "农业物联网", "精准农业"], "subsystems": ["物联网平台", "环境监测", "大数据平台"]},
    "智慧旅游": {"keywords": ["智慧旅游", "智慧景区", "旅游服务"], "subsystems": ["信息发布", "视频监控", "一卡通"]},
    
    # 商业级
    "智慧零售": {"keywords": ["智慧零售", "智慧商超", "新零售"], "subsystems": ["视频监控", "一卡通", "信息发布"]},
    "智慧金融": {"keywords": ["智慧金融", "金融科技", "智慧银行"], "subsystems": ["安防系统", "视频监控", "门禁通行"]},
    "智慧医疗": {"keywords": ["智慧医疗", "医疗信息化", "互联网医疗"], "subsystems": ["物联网平台", "大数据平台", "云平台"]},
    "智慧教育": {"keywords": ["智慧教育", "在线教育", "教育信息化"], "subsystems": ["云平台", "大数据平台", "广播系统"]},
    
    # 生活级
    "智慧养老": {"keywords": ["智慧养老", "智慧康养", "居家养老"], "subsystems": ["物联网平台", "安防系统", "一卡通"]},
    "智慧家居": {"keywords": ["智能家居", "智慧家装", "全屋智能"], "subsystems": ["照明系统", "环境监测", "物联网平台"]},
    "智慧酒店": {"keywords": ["智慧酒店", "智能酒店", "酒店信息化"], "subsystems": ["一卡通", "楼宇自控", "信息发布"]},
    "智慧场馆": {"keywords": ["智慧场馆", "智慧体育", "会展中心"], "subsystems": ["安防系统", "广播系统", "照明系统"]},
    
    # 交通枢纽
    "智慧机场": {"keywords": ["智慧机场", "机场信息化", "智慧航站"], "subsystems": ["安防系统", "信息发布", "物联网平台"]},
    "智慧港口": {"keywords": ["智慧港口", "智能码头", "港口物流"], "subsystems": ["物联网平台", "大数据平台", "视频监控"]},
    
    # 工业级
    "智慧矿山": {"keywords": ["智慧矿山", "智能采矿", "矿山安全"], "subsystems": ["物联网平台", "环境监测", "指挥中心"]},
    "智慧油田": {"keywords": ["智慧油田", "智能采油", "油田物联网"], "subsystems": ["物联网平台", "大数据平台", "环境监测"]},
    "智慧管网": {"keywords": ["智慧管网", "管网监测", "地下管网"], "subsystems": ["物联网平台", "大数据平台", "环境监测"]},
    
    # 应急级
    "智慧应急": {"keywords": ["智慧应急", "应急指挥", "应急管理"], "subsystems": ["指挥中心", "物联网平台", "大数据平台"]},
    
    # 文旅级
    "智慧文旅": {"keywords": ["智慧文旅", "文旅融合", "全域旅游"], "subsystems": ["信息发布", "一卡通", "视频监控"]},
    "智慧体育": {"keywords": ["智慧体育", "智慧运动", "体育信息化"], "subsystems": ["一卡通", "信息发布", "照明系统"]},
    "智慧传媒": {"keywords": ["智慧传媒", "融媒体", "智慧广电"], "subsystems": ["广播系统", "信息发布", "云平台"]},
    
    # 其他
    "智慧气象": {"keywords": ["智慧气象", "气象服务", "气象监测"], "subsystems": ["环境监测", "物联网平台", "大数据平台"]},
    "智慧地质": {"keywords": ["智慧地质", "地质监测", "地质灾害"], "subsystems": ["物联网平台", "环境监测", "大数据平台"]},
    "智慧海洋": {"keywords": ["智慧海洋", "海洋监测", "海洋经济"], "subsystems": ["物联网平台", "大数据平台", "环境监测"]},
}

# ============================================
# 智能化子系统（31个）
# ============================================

SMART_SUBSYSTEMS = {
    # 基础设施类
    "综合布线": {"keywords": ["光纤", "网线", "配线架", "桥架", "弱电"], "domain": ["智慧城市", "智慧园区", "智慧建筑"]},
    "机房工程": {"keywords": ["服务器", "机柜", "UPS", "精密空调", "数据中心"], "domain": ["智慧城市", "智慧园区"]},
    "数据中心": {"keywords": ["IDC", "云计算中心", "服务器"], "domain": ["智慧城市", "智慧园区"]},
    "云平台": {"keywords": ["云计算", "云服务", "公有云", "私有云"], "domain": ["智慧城市", "智慧园区"]},
    "指挥中心": {"keywords": ["运营中心", "调度中心", "城市运行中心"], "domain": ["智慧城市", "智慧应急"]},
    
    # 安防类
    "安防系统": {"keywords": ["安防", "安全防范", "安保系统"], "domain": ["智慧城市", "智慧园区", "智慧社区"]},
    "视频监控": {"keywords": ["摄像头", "CCTV", "NVR", "监控", "视频"], "domain": ["智慧城市", "智慧园区", "智慧社区"]},
    "入侵报警": {"keywords": ["报警", "入侵", "防盗", "周界"], "domain": ["智慧园区", "智慧社区"]},
    "出入口控制": {"keywords": ["门禁", "道闸", "出入口"], "domain": ["智慧园区", "智慧社区"]},
    "电子巡更": {"keywords": ["巡更", "巡逻", "巡检"], "domain": ["智慧园区", "智慧社区"]},
    
    # 通行类
    "门禁通行": {"keywords": ["门禁", "闸机", "通行"], "domain": ["智慧园区", "智慧社区", "智慧建筑"]},
    "停车管理": {"keywords": ["停车场", "车位", "停车"], "domain": ["智慧园区", "智慧社区", "智慧停车"]},
    "停车场管理": {"keywords": ["停车场", "车场管理"], "domain": ["智慧停车"]},
    "智能卡": {"keywords": ["IC卡", "智能卡", "RFID"], "domain": ["智慧园区", "智慧社区"]},
    "一卡通": {"keywords": ["一卡通", "通卡", "卡系统"], "domain": ["智慧园区", "智慧社区", "智慧学校"]},
    
    # 楼控类
    "楼宇自控": {"keywords": ["BAS", "BA系统", "楼控", "DDC"], "domain": ["智慧建筑", "智慧园区"]},
    "照明系统": {"keywords": ["照明", "灯光", "智能照明"], "domain": ["智慧建筑", "智慧园区", "智慧路灯"]},
    "能耗管理": {"keywords": ["能耗", "节能", "能源"], "domain": ["智慧建筑", "智慧园区", "智慧能源"]},
    "环境监测": {"keywords": ["环境", "监测", "传感器"], "domain": ["智慧建筑", "智慧环保"]},
    
    # 机电类
    "暖通空调": {"keywords": ["HVAC", "空调", "暖通"], "domain": ["智慧建筑", "智慧园区"]},
    "给排水": {"keywords": ["给水", "排水", "水泵"], "domain": ["智慧建筑", "智慧水务"]},
    "供配电": {"keywords": ["配电", "电力", "供电"], "domain": ["智慧建筑", "智慧电网"]},
    "电梯系统": {"keywords": ["电梯", "扶梯"], "domain": ["智慧建筑", "智慧园区"]},
    "电梯监控": {"keywords": ["电梯监控", "电梯管理"], "domain": ["智慧建筑"]},
    
    # 消防类
    "消防系统": {"keywords": ["消防", "火灾", "喷淋"], "domain": ["智慧建筑", "智慧园区", "智慧消防"]},
    
    # 通信类
    "广播系统": {"keywords": ["广播", "背景音乐", "公共广播"], "domain": ["智慧建筑", "智慧园区"]},
    "会议系统": {"keywords": ["会议", "音视频", "视频会议"], "domain": ["智慧建筑", "智慧园区"]},
    "信息发布": {"keywords": ["信息发布", "LED", "导引"], "domain": ["智慧城市", "智慧园区"]},
    
    # 平台类
    "物联网平台": {"keywords": ["IoT", "物联网", "传感器"], "domain": ["智慧城市", "智慧园区"]},
    "大数据平台": {"keywords": ["大数据", "数据中台", "数据分析"], "domain": ["智慧城市", "智慧园区"]},
}

# ============================================
# 获取所有领域列表
# ============================================

def get_all_domains():
    """获取所有智慧领域列表"""
    return list(SMART_DOMAINS.keys())

def get_all_subsystems():
    """获取所有子系统列表"""
    return list(SMART_SUBSYSTEMS.keys())

def get_domain_keywords(domain: str) -> list:
    """获取某个领域的关键词"""
    if domain in SMART_DOMAINS:
        return SMART_DOMAINS[domain].get("keywords", [])
    return []

def get_subsystem_keywords(subsystem: str) -> list:
    """获取某个子系统的关键词"""
    if subsystem in SMART_SUBSYSTEMS:
        return SMART_SUBSYSTEMS[subsystem].get("keywords", [])
    return []

def get_subsystem_domains(subsystem: str) -> list:
    """获取某个子系统适用的领域"""
    if subsystem in SMART_SUBSYSTEMS:
        return SMART_SUBSYSTEMS[subsystem].get("domain", [])
    return []

def classify_content(title: str, content: str) -> dict:
    """
    根据内容自动分类
    
    Returns:
        {
            "domain": "智慧城市",  # 主要领域
            "subsystem": "安防系统",  # 主要子系统
            "all_domains": ["智慧城市", "智慧园区"],  # 所有匹配的领域
            "all_subsystems": ["安防系统", "视频监控"]  # 所有匹配的子系统
        }
    """
    text = f"{title} {content}"
    
    # 匹配领域
    matched_domains = []
    for domain, info in SMART_DOMAINS.items():
        keywords = info.get("keywords", [])
        if any(kw in text for kw in keywords):
            matched_domains.append(domain)
    
    # 匹配子系统
    matched_subsystems = []
    for subsystem, info in SMART_SUBSYSTEMS.items():
        keywords = info.get("keywords", [])
        if any(kw in text for kw in keywords):
            matched_subsystems.append(subsystem)
    
    return {
        "domain": matched_domains[0] if matched_domains else "智慧城市",
        "subsystem": matched_subsystems[0] if matched_subsystems else "",
        "all_domains": matched_domains,
        "all_subsystems": matched_subsystems
    }

def get_storage_path(domain: str, subsystem: str = "") -> str:
    """
    获取文档存储路径
    
    Args:
        domain: 智慧领域
        subsystem: 子系统（可选）
    
    Returns:
        存储路径，如 "docs/智慧类领域/智慧城市/安防系统/"
    """
    base_path = f"docs/智慧类领域/{domain}"
    if subsystem:
        base_path += f"/{subsystem}"
    return base_path


# ============================================
# 导出配置
# ============================================

if __name__ == "__main__":
    print("📊 智慧城市知识库分类配置")
    print("=" * 50)
    print(f"智慧类领域: {len(SMART_DOMAINS)} 个")
    print(f"智能化子系统: {len(SMART_SUBSYSTEMS)} 个")
    print()
    print("领域列表:")
    for i, domain in enumerate(SMART_DOMAINS.keys(), 1):
        print(f"  {i:2d}. {domain}")
    print()
    print("子系统列表:")
    for i, subsystem in enumerate(SMART_SUBSYSTEMS.keys(), 1):
        print(f"  {i:2d}. {subsystem}")
