# -*- coding: utf-8 -*-
"""BMS 算法追踪 2026-08-17 周报生成器"""

DATE = "2026-08-17"

# Admiralty / NATO AJP-2.1: dual-character rating, e.g. "B2"
# Source Reliability A-F badge colors
TIER_BG = {"A": "#6abf69", "B": "#4a90d9", "C": "#e67e22", "D": "#9b59b6",
           "E": "#9b59b6", "F": "#95a5a6"}


def badge(kind, text):
    if kind == "tier":
        return ('<span style="background:%s;color:#fff;font-size:11px;padding:1px 6px;'
                'border-radius:3px;">%s</span>' % (TIER_BG[text[0]], text))
    if kind == "date":
        return ('<span style="background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 6px;'
                'border-radius:3px;">\U0001F4C5%s</span>' % text)
    return ('<span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;'
            'border-radius:3px;">%s</span>' % text)


def tag_row(tier, date, *tags):
    parts = [badge("tier", tier), badge("date", date)] + [badge("tag", t) for t in tags]
    return ('<div style="display:flex;align-items:center;flex-wrap:nowrap;gap:4px;margin-bottom:6px;'
            'overflow-x:auto;white-space:nowrap;">%s</div>' % "".join(parts))


def src(url):
    if isinstance(url, str):
        url = [url]
    spans = "".join(
        '<span style="color:#4a90d9;text-decoration:none;word-break:break-all">%s</span>' % u
        for u in url)
    return '<div style="color:#888;font-size:12px;">来源: %s</div>' % spans


def entry(border, tags_html, num, title, fields, url):
    flds = "".join(
        '<div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">%s <b>%s:</b>%s</div>'
        % (icon, label, text) for icon, label, text in fields)
    return ('<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid %s;'
            'border-radius:4px;word-break:break-all;">%s'
            '<div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">'
            '%d · %s</div>%s%s</section>' % (border, tags_html, num, title, flds, src(url)))


def paper(n, tier, date, journal, topic, title, abstract, innovation, url):
    return entry("#4a90d9", tag_row(tier, date, journal, topic), n, title,
                 [("\U0001F4CC", "摘要", abstract), ("\U0001F4A1", "创新", innovation)], url)


def vendor(n, tier, date, t1, t2, title, abstract, url):
    return entry("#27ae60", tag_row(tier, date, t1, t2), n, title,
                 [("\U0001F4CC", "摘要", abstract)], url)


def opensrc(n, date, t1, t2, title, abstract, url):
    return entry("#4a90d9", tag_row("C2", date, t1, t2), n, title,
                 [("\U0001F4CC", "摘要", abstract)], url)


def patent(n, tier, date, t1, t2, title, holder, abstract, innovation, url):
    return entry("#e67e22", tag_row(tier, date, t1, t2), n, title,
                 [("\U0001F464", "申请人", holder), ("\U0001F4CC", "摘要", abstract),
                  ("\U0001F4A1", "创新", innovation)], url)


def standard(n, tier, date, t1, t2, title, purpose, core, impl, url):
    return entry("#e67e22", tag_row(tier, date, t1, t2), n, title,
                 [("\U0001F3AF", "目的", purpose), ("\U0001F4D1", "核心内容", core),
                  ("\U0001F680", "实施", impl)], url)


def h2(text):
    return ('<h2 style="font-size:19px;color:#111;margin:24px 0 12px 0;padding-bottom:8px;'
            'border-bottom:2px solid #4a90d9;font-weight:bold;text-align:left;">%s</h2>' % text)


trends = [
    ("物理信息AI成为电池状态估计主流范式",
     "本周多篇论文与专利聚焦PINN、KAN、物理约束Transformer等数据-物理融合方法，纯数据驱动路线让位于可解释、可外推的混合建模。"),
    ("储能订单潮延续，行业集中度加速提升",
     "宁德时代再获3GWh海外大单，融捷能源签4GWh框架协议，中国能建30GWh集采公示36家入围，头部厂商凭借交付与成本优势持续收割份额。"),
    ("新型储能标准本周密集立项征求意见",
     "中电联一周内发布十余项储能类标准征求意见函，覆盖压缩空气储能全链条与电动汽车充放电资源；锂电储能系统CCC强制认证8月11日正式生效。"),
    ("固态与钠电产业化信号密集",
     "Nature Energy揭示固态电解质电子电导引发自放电的新机制，吉利明确加快固态/钠电研发，亿纬锂能钠电斩获产业化先锋奖并计划年底批量交付。"),
    ("安全监测技术向多模态传感演进",
     "压力信号析锂量化、稀疏电压故障解码、快充核心温度估计等研究集中涌现，热失控预警从单一气体检测走向压力/温度/电压多模态融合。"),
]

papers = [
    dict(tier="A2", date="2026-08-17", journal="Nature Energy", topic="固态电池",
         title="固态电解质电子电导导致全固态电池物理自放电",
         abstract="揭示固态电解质的电子电导率会在电池内部形成泄漏通道，引发全固态电池的物理自放电，量化其对荷电保持能力的侵蚀。",
         innovation="将自放电归因于电解质本征电子泄漏，为固态电池BMS的SOC校准、漏电诊断与存储策略提供全新理论依据。",
         url="https://doi.org/10.1038/s41560-026-02090-x"),
    dict(tier="A2", date="2026-08-17", journal="Nature Energy", topic="电极过程",
         title="无扩散机制在电池颗粒中产生类扩散电化学行为",
         abstract="发现电池活性颗粒内无需离子扩散也能产生形似扩散的电化学响应，挑战以菲克扩散为核心的传统解释框架。",
         innovation="为电极过程建模与阻抗谱解释提供新视角，直接影响BMS等效电路与电化学模型的参数辨识策略。",
         url="https://doi.org/10.1038/s41560-026-02123-5"),
    dict(tier="B2", date="2026-08-11", journal="Advanced Science", topic="安全监测",
         title="基于压力信号量化析锂程度的锂电池安全评估",
         abstract="利用充电过程中电极膨胀产生的压力信号，量化锂离子电池析锂程度，建立压力特征与安全风险的映射关系。",
         innovation="将压力传感引入BMS安全监测链路，为析锂早期识别与快充安全边界动态调整提供可植入的测量手段。",
         url="https://doi.org/10.1002/advs.77129"),
    dict(tier="B2", date="2026-08-10", journal="Energy Material Advances", topic="老化诊断",
         title="跨场景与跨材料体系的电池老化诊断",
         abstract="在对比鲜明的服役场景与材料组分下系统开展电池老化诊断研究，覆盖不同温度、倍率与正极材料组合。",
         innovation="建立跨体系老化诊断方法学，支撑多材料混装电池包的SOH统一估计与剩余寿命预测。",
         url="https://doi.org/10.34133/energymatadv.0380"),
    dict(tier="B2", date="2026-08-16", journal="ACS Energy Letters", topic="钠离子电池",
         title="双重驱动的正极界面调控助力长寿命钠离子电池",
         abstract="通过双重驱动策略同步调控钠离子电池正极电解质界面（CEI）的组成与结构，显著提升长循环耐久性。",
         innovation="面向钠电产业化的界面工程方案，与本周亿纬锂能钠电量产提速消息形成技术呼应。",
         url="https://doi.org/10.1021/acsenergylett.6c02224"),
    dict(tier="B2", date="2026-08-13", journal="ACS Energy Letters", topic="表征标准",
         title="电池体系原位衍射研究的标准化",
         abstract="提出电池系统operando衍射研究的标准化框架，统一实验设计、数据采集与分析流程。",
         innovation="原位表征标准化将催生可信的老化机理数据集，为BMS算法训练与机理模型验证提供高质量数据底座。",
         url="https://doi.org/10.1021/acsenergylett.6c01791"),
    dict(tier="C3", date="2026-08-12", journal="arXiv", topic="快充安全",
         title="基于Kolmogorov-Arnold网络的电池核心温度估计提升快充安全性",
         abstract="提出以KAN网络替代传统MLP的电池核心温度软测量方法，从表面温度与工况特征推断内部温度。",
         innovation="KAN的表达能力带来更高精度的核心温度估计，为快充电流调控与热安全边界提供关键输入。",
         url="https://arxiv.org/abs/2608.12638"),
    dict(tier="C3", date="2026-08-11", journal="arXiv", topic="故障诊断",
         title="跨模态拓扑从稀疏电压快照解码电池故障",
         abstract="构建跨模态拓扑表征方法，仅凭稀疏采样的电压快照即可识别电池单体级异常与故障模式。",
         innovation="在降低采样频率的条件下保持故障检出能力，可显著削减BMS数据采集、存储与传输负担。",
         url="https://arxiv.org/abs/2608.10825"),
    dict(tier="C3", date="2026-08-10", journal="arXiv", topic="PHM综述",
         title="物理信息机器学习在预测性健康管理中的系统综述",
         abstract="系统梳理物理信息机器学习（PIML）在PHM领域的模型范式、嵌入方式与应用效果，覆盖电池等关键对象。",
         innovation="给出数据-物理融合方法的标准化路线图，指明电池RUL/SOH预测从实验室走向车端的可信化路径。",
         url="https://arxiv.org/abs/2608.10047"),
    dict(tier="C3", date="2026-08-14", journal="arXiv", topic="换电策略",
         title="非合作换电站的最优定价与充电策略设计",
         abstract="针对多个利益独立的换电站构成的非合作博弈场景，联合设计电价策略与电池充电调度方案。",
         innovation="博弈论框架下实现定价与充电的纳什均衡求解，为换电网络运营与电池资产调度提供决策工具。",
         url="https://arxiv.org/abs/2608.14167"),
]

vendors = [
    dict(tier="C2", date="2026-08-17", t1="储能集采", t2="中国能建",
         title="中国能建30GWh储能系统集采公示：36家企业入围，宁德时代多标段领跑",
         abstract="2026年度磷酸铁锂储能系统集采中标候选人公示，总规模30GWh分四个标段，宁德时代全部标段入围，亿纬动力、中创新航、楚能新能源等分食其余份额。",
         url=["https://m.bjx.com.cn/mnews/20260817/1508654.shtml",
              "https://mchuneng.in-en.com/html/chunengy-57205.shtml"]),
    dict(tier="B2", date="2026-08-11", t1="海外订单", t2="宁德时代",
         title="宁德时代与ContourGlobal签署3GWh储能供应协议",
         abstract="国际独立发电商ContourGlobal宣布与宁德时代签署3GWh电池储能系统供应协议，将采购526个集装箱液冷储能系统，海外大储订单持续向中国龙头集中。",
         url="https://finance.sina.com.cn/roll/2026-08-11/doc-inimxvum4255503.shtml"),
    dict(tier="C2", date="2026-08-17", t1="框架协议", t2="融捷能源",
         title="融捷能源与Lineage Power签署2027年4GWh框架合作协议",
         abstract="基于Lineage Power对2027年储能项目的需求规划，拟采购合计4GWh的314Ah及588Ah电芯，应用于大型储能与工商业储能场景，融捷近两月海外签约累计突破20GWh。",
         url="https://m.bjx.com.cn/mnews/20260817/1508813.shtml"),
    dict(tier="C2", date="2026-08-11", t1="合资调整", t2="三星SDI",
         title="三星SDI收购通用所持美国电池合资公司全部股权",
         abstract="因电动车需求不及预期，三星SDI宣布解除与通用汽车的印第安纳州合资业务，收购通用所持49.99%股权，工厂将转产储能系统与电动车多元应用电池。",
         url="https://www.marklines.com/cn/news/tag/181/ev-battery"),
    dict(tier="D3", date="2026-08-16", t1="数据中心储能", t2="LG新能源",
         title="LG新能源将为谷歌最大光储一体化项目供应电池",
         abstract="谷歌与Cypress Creek在阿肯色州联合宣布Steel River能源中心项目，LG新能源将为其供应电池，进一步扩张AI数据中心驱动的储能基建业务。",
         url="https://gmteight.com/flash/detail/1472499"),
    dict(tier="C2", date="2026-08-14", t1="钠电产业化", t2="亿纬锂能",
         title="亿纬锂能获2026钠电产业化先锋奖，年底批量交付钠电产品",
         abstract="高工钠电产业峰会上，亿纬锂能展示NFPP钠电产品矩阵：主力NF155L电芯支持-40℃~60℃宽温域、3万次循环、系统零热失控，计划2026年底实现钠电批量交付。",
         url="https://www.evebattery.com/news-1104"),
    dict(tier="B2", date="2026-08-17", t1="中期业绩", t2="吉利",
         title="吉利中期业绩会：加快固态电池、钠电池及大容量储能产品研发",
         abstract="吉利汽车2026年中期业绩会上，CEO安聪慧表示上半年营收超1700亿元、核心归母净利增长46%，电池业务将聚焦主力电芯开发，加快固态、钠电与大容量储能布局。",
         url="https://finance.sina.com.cn/roll/2026-08-17/doc-ininrqsh0065415.shtml"),
    dict(tier="B2", date="2026-08-17", t1="资本运作", t2="湖南裕能",
         title="湖南裕能递交港交所招股书，冲刺磷酸铁锂正极A+H",
         abstract="湖南裕能向香港联交所递交H股上市申请，中信建投国际与汇丰联席保荐；2025年磷酸盐正极收入339.1亿元、占比约97%，募资将投向产能与技术升级。",
         url="https://data.eastmoney.com/notices/detail/H2113/AN202608171828035056.html"),
    dict(tier="B2", date="2026-08-16", t1="行业研报", t2="国信证券",
         title="国信证券：锂电Q2业绩延续向上，电池企业屡获海外储能订单",
         abstract="锂电产业链双周报指出，Q2电池企业业绩延续向上趋势，海外储能需求旺盛，宁德时代、海辰储能、融捷能源等接连斩获欧洲、澳洲、印度大单。",
         url="https://pdf.dfcfw.com/pdf/H3_AP202608161828030034_1.pdf"),
    dict(tier="C3", date="2026-08-16", t1="供应链", t2="楚能新能源",
         title="楚能新能源电解液供应协议上调至101万吨，储能签约累计超60GWh",
         abstract="企查查企业动态更新显示，楚能新能源与天赐材料子公司签订电解液供应补充协议，供应量由55万吨上调至101万吨至2030年底；SNEC 2026展会斩获12GWh储能订单，一个月内累计签约突破60GWh。",
         url="https://www.qcc.com/creport/172e0c3a8430b289bf29b236d03c066f.html"),
]

oss = [
    dict(date="2026-08-17", t1="硬件BMS", t2="ESP32",
         title="openups：ESP32-S3智能锂电池UPS控制系统",
         abstract="基于ESP32-S3的开源BMS，采用BQ24780S/BQ24800充电管理与BQ76920电池监控芯片，支持3-5串锂电/磷酸铁锂、12-19V宽压输入，可接入Home Assistant与米家。",
         url="https://github.com/sayhellotojungle/openups"),
    dict(date="2026-08-17", t1="RUL预测", t2="数字孪生",
         title="电池剩余寿命预测数字孪生框架",
         abstract="融合机器学习、集成学习与电池退化分析，构建带数字孪生界面的RUL预测工作流，覆盖特征工程、模型训练与可视化全链路。",
         url="https://github.com/Next-Gen-Coder-2007/Intelligent-Lithium-Ion-Battery-Remaining-Useful-Life-Prediction-Digital-Twin"),
    dict(date="2026-08-15", t1="数据集", t2="固态电池",
         title="Scandium Labs固态电池电解质材料数据集",
         abstract="面向机器学习即用的固态电池电解质材料数据集，覆盖全部8类固态电解质体系，为固态电池材料筛选与性能预测提供统一数据底座。",
         url="https://github.com/ScandiumLabs-in/Scandium-Labs-Solid-State-Battery-Dataset"),
    dict(date="2026-08-16", t1="SOC估计", t2="MATLAB",
         title="EV电池SOC估计：集成学习与前馈网络对比",
         abstract="MATLAB流水线，在实车工况数据上对比集成方法与前馈神经网络的SOC估计精度，附带完整预处理与评估脚本，适合作为算法基线复现。",
         url="https://github.com/sanusiaz/matlab-state-of-charge-EV-battery-management"),
    dict(date="2026-08-16", t1="失效预测", t2="NASA数据",
         title="多时间尺度电池失效风险分层模型",
         abstract="在NASA 18650电池数据上扩展多时间尺度风险分类框架，按预测提前期分层输出失效概率，支撑BMS分级预警策略设计。",
         url="https://github.com/touhidsiddiqueeraj-bit/Multi-Horizon-Hazard-Models-for-Battery-Failure-Prediction"),
    dict(date="2026-08-14", t1="数据集", t2="制造监测",
         title="电池极耳激光焊接原位监测数据集",
         abstract="发布带原位监测信号的电池极耳激光焊接数据集，可用于焊接质量在线判别与工艺参数优化，是电池制造环节少见的开源数据。",
         url="https://github.com/ARTS-Laboratory/Dataset-battery-tab-laser-welding"),
    dict(date="2026-08-17", t1="卡尔曼滤波", t2="Simulink",
         title="64串16并电池模型与卡尔曼滤波SOC估计",
         abstract="MATLAB/Simulink实现戴维南等效电路、热模型与卡尔曼滤波SOC估计的完整电池包仿真（64S16P），可直接用于算法在环验证。",
         url="https://github.com/arsalaan-mit/64S16P-Battery-Model-with-kalman-filter-soc-approximation-"),
    dict(date="2026-08-17", t1="生产级AI", t2="电动船舶",
         title="daluyan-ml：电动渡轮生产级电池AI模型",
         abstract="为M/B Daluyan电动渡轮部署的5个生产级XGBoost模型：行程SOC误差0.687%、实时SOC误差0.325%、电机异常检测准确率96%以上，车规外场景落地参考。",
         url="https://github.com/FreddieJr-stud/daluyan-ml"),
    dict(date="2026-08-17", t1="实时BMS", t2="STM32",
         title="双STM32架构实时EV电池管理与安全系统",
         abstract="采用双STM32冗余架构的实时电动汽车BMS设计，涵盖充放电保护、故障检测与安全联动的完整嵌入式实现，附原理图与固件代码。",
         url="https://github.com/abhayakhade0/CDAC-Project-Realtime-EV-Management-System-with-Safety-Protections"),
    dict(date="2026-08-14", t1="SOH预测", t2="机器学习",
         title="EV电池健康度机器学习预测项目",
         abstract="基于机器学习的电动汽车电池SOH预测，包含数据清洗、健康特征提取与多模型对比，适合作为SOH算法快速原型基线。",
         url="https://github.com/Nikhil-jaiswal007/EV-battery-health-prediction"),
]

patents = [
    dict(date="2026-08-15", t1="液流电池", t2="宁德时代",
         title="半固态液流电池、正极悬浮液、储能装置及用电装置（CN122552572A）",
         holder="宁德时代新能源科技股份有限公司、深圳大学",
         abstract="申请公布一种半固态液流电池及其正极悬浮液配方，通过改善悬浮稳定性提升半固态液流电池的电化学性能。",
         innovation="正极悬浮液体系创新有助于长时储能电池的能量密度与循环寿命提升。",
         url="https://patents.google.com/patent/CN122552572A/zh"),
    dict(date="2026-08-16", t1="PINN", t2="状态预测",
         title="基于PINN的电池状态预测与充放电控制系统和方法（CN122577329A）",
         holder="杭州科工电子科技股份有限公司",
         abstract="将物理信息神经网络引入电池状态预测，并与充放电控制联合管控，实现电池安全边界内的状态估计和功率调度。",
         innovation="PINN把电化学机理嵌入网络训练，小样本条件下即可获得可解释的状态预测，直击BMS冷启动数据不足痛点。",
         url="https://patents.google.com/patent/CN122577329A/zh"),
    dict(date="2026-08-16", t1="电池安全", t2="宁德时代",
         title="电池装置及用电装置（CN224637347U）",
         holder="宁德时代新能源科技股份有限公司",
         abstract="授权公告一种电池装置结构设计，通过防护与泄压路径优化降低电池起火爆炸风险。",
         innovation="结构级安全冗余设计，为高能量密度电池包的机械滥用防护提供方案。",
         url=["https://finance.sina.com.cn/stock/aigc/zl/2026-08-16/doc-ininnkft1592323.shtml",
              "https://patents.google.com/patent/CN224637347U/zh"]),
    dict(date="2026-08-16", t1="充电控制", t2="宁德时代",
         title="电池装置充电方法、装置、系统及电池装置（CN121663004B）",
         holder="宁德时代新能源科技股份有限公司、宁德时代润智软件科技有限公司",
         abstract="授权专利提供电池装置充电方法，可精准控制电池加热与充电过程，减少能量损耗并提升充电安全与需求匹配度。",
         innovation="加热-充电协同控制策略，兼顾低温快充效率与寿命保护。",
         url="https://patents.google.com/patent/CN121663004B/zh"),
    dict(date="2026-08-16", t1="电池系统", t2="SOC均衡",
         title="电池单体、电池装置、用电装置及储能装置（CN122512122A）",
         holder="宁德时代新能源科技股份有限公司",
         abstract="申请公布电池系统相关专利，据报道可实现电池簇荷电状态均衡并降本提效，覆盖单体到系统多层级设计。",
         innovation="电池簇级SOC均衡管理有助于延缓储能系统木桶效应、提升全寿命放电量。",
         url="https://patents.google.com/patent/CN122512122A/zh"),
    dict(date="2026-08-16", t1="结构设计", t2="宁德时代",
         title="电池装置和用电设备（CN224637379U）",
         holder="宁德时代新能源科技股份有限公司",
         abstract="授权公告一种电池装置结构，通过布局优化提升电池装置自身空间利用率。",
         innovation="单位体积能量密度提升方案，直接改善成组效率。",
         url="https://patents.google.com/patent/CN224637379U/zh"),
    dict(date="2026-08-16", t1="绝缘防护", t2="宁德时代",
         title="电池单体、绝缘片、电池单体组件及电池装置（CN224637383U）",
         holder="宁德时代新能源科技股份有限公司",
         abstract="授权公告带强度减弱部的绝缘片设计，可防止绝缘片翘曲，提升电池绝缘与外观质量。",
         innovation="绝缘片防翘结构降低装配不良率，保障高压安全裕度。",
         url="https://patents.google.com/patent/CN224637383U/zh"),
    dict(date="2026-08-16", t1="制造工艺", t2="宁德时代",
         title="电极组件加工装置及电池生产设备（CN224637196U）",
         holder="宁德时代新能源科技股份有限公司",
         abstract="授权公告一种电极组件加工装置，通过热熔连接隔离件提升电池产品质量与生产一致性。",
         innovation="工艺装备创新支撑电芯良率与一致性，间接降低BMS个体差异补偿负担。",
         url="https://patents.google.com/patent/CN224637196U/zh"),
    dict(date="2026-08-16", t1="激光清洗", t2="制造装备",
         title="激光清洗装置及方法（CN122007093A）",
         holder="宁德时代新能源科技股份有限公司",
         abstract="申请公布一种极片激光清洗装置，通过光路稳定性设计提升极片激光清洗的稳定性与合格率。",
         innovation="清洗一致性提升可减少极片金属异物，降低自放电与短路风险。",
         url="https://patents.google.com/patent/CN122007093A/zh"),
    dict(tier="C3", date="2026-08-14", t1="结构密封", t2="海辰储能",
         title="端盖组件及储能装置（发明专利授权）",
         holder="厦门海辰储能科技股份有限公司",
         abstract="授权公告一种储能电池端盖组件设计，优化密封与防护结构以提升储能装置长期运行可靠性。",
         innovation="端盖级结构创新配合其1175Ah长时储能电芯，支撑长时储能系统安全寿命。",
         url="https://www.qcc.com/crun/d60d89f858e4f16d66263da76d2f8b7c.html"),
]

standards = [
    dict(tier="B2", date="2026-08-17", t1="充电协议", t2="中电联",
         title="《电动汽车传导充电互操作性测试规范》等两项国标征求意见",
         purpose="统一车桩互操作与通信协议测试方法，解决充电兼容性与BMS通信一致性问题。",
         core="规定传导充电互操作测试流程，以及非车载充电机与BMS之间通信协议一致性测试要求。",
         impl="公开征求意见阶段，产业链企业可向中电联反馈技术意见。",
         url=["https://www.chinaev100.com/focus/detail/485", "https://standard.cec.org.cn/advice/list"]),
    dict(tier="A2", date="2026-08-11", t1="强制认证", t2="认监委",
         title="锂离子电池储能系统纳入CCC强制认证并正式生效",
         purpose="将家用与工商业锂电储能系统（含电池包、BMS、PCS集成系统）纳入强制性市场准入监管。",
         core="依据GB/T 34131等标准开展关键安全指标测试与产品一致性检查，覆盖0916储能系统等新增强制品类。",
         impl="2026年8月11日起执行，无认证产品将禁止上市销售。",
         url="https://www.cnca.gov.cn/hlwfw/ywzl/qzxcprz/ssgz/art/2026/art_5261f654e02d45edaf0805fb268c9fc9.html"),
    dict(tier="B2", date="2026-08-17", t1="新型储能", t2="防火设计",
         title="《压缩空气储能电站设计防火标准》电力行业标准征求意见",
         purpose="填补压缩空气储能电站防火设计标准空白，防范新型储能电站火灾风险。",
         core="规定储能电站防火分区、安全间距、消防设施与监测报警系统的设计要求。",
         impl="中电联标准化平台公开征求意见，行业单位可提交修改建议。",
         url="https://standard.cec.org.cn/advice/list"),
    dict(tier="B2", date="2026-08-17", t1="新型储能", t2="节能设计",
         title="《压缩空气储能电站节能设计规范》电力行业标准征求意见",
         purpose="规范压缩空气储能电站节能设计，提升系统综合效率与经济性。",
         core="涵盖储换热系统效率、电耗指标与设备选型的节能设计要求。",
         impl="处于征求意见阶段，与同批多项压缩空气储能标准协同推进。",
         url="https://standard.cec.org.cn/advice/list"),
    dict(tier="B2", date="2026-08-14", t1="车网互动", t2="充放电资源",
         title="《电动汽车充放电资源规划计算规范》电力行业标准征求意见",
         purpose="为电动汽车作为分布式充放电资源的电网规划提供统一计算方法。",
         core="规定电动汽车充放电资源的建模、规模测算与电网影响计算规范，支撑V2G有序接入。",
         impl="征求意见中，是车网互动标准体系的关键一环。",
         url="https://standard.cec.org.cn/advice/list"),
    dict(tier="B2", date="2026-08-11", t1="飞轮储能", t2="监造导则",
         title="《电力储能用飞轮本体监造导则》电力行业标准征求意见",
         purpose="建立飞轮储能本体设备监造的统一技术依据，保障新型储能装备质量。",
         core="规定飞轮本体制造过程的关键工序见证、检验项目与监造文件要求。",
         impl="中电联标准征求意见阶段，面向飞轮储能制造与业主单位。",
         url="https://standard.cec.org.cn/advice/list"),
    dict(tier="C2", date="2026-08-11", t1="压缩空气", t2="选址规程",
         title="《压缩空气储能电站选址技术规程》征求意见",
         purpose="统一压缩空气储能电站选址的技术评价方法与安全准则。",
         core="涵盖地质条件、储气库适宜性、电网接入与外部安全防护距离等选址要素。",
         impl="中电联团体标准（非电力行业标准），与同批压缩空气储能系列标准协同推进。",
         url="https://standard.cec.org.cn/advice/list"),
    dict(tier="C2", date="2026-08-11", t1="压缩空气", t2="安全监测",
         title="《压缩空气储能电站地下储气库安全监测设计规范》征求意见",
         purpose="防范地下储气库运行风险，为压缩空气储能电站安全监测提供设计标准。",
         core="规定储气库围岩变形、气密性、温度与压力等监测项目及测点布置要求。",
         impl="中电联团体标准（非电力行业标准），适用于新建及改扩建压缩空气储能项目。",
         url="https://standard.cec.org.cn/advice/list"),
    dict(tier="C2", date="2026-08-12", t1="功率器件", t2="IGBT",
         title="《压接型IGBT器件热阻测试方法》中电联标准征求意见",
         purpose="统一压接型IGBT器件热阻测试方法，服务储能变流器功率器件可靠性评估。",
         core="规定测试电路、结温测量、热阻计算与数据处理的标准化流程。",
         impl="中电联团体标准（非电力行业标准），为PCS与BMS功率环节的器件选型提供依据。",
         url="https://standard.cec.org.cn/advice/list"),
    dict(tier="A2", date="2026-08-17", t1="火灾预警", t2="即将实施",
         title="GB/T 46261-2025《电化学储能电站火灾监测预警系统通用技术要求》进入实施倒计时",
         purpose="规范电化学储能电站火灾监测预警系统的设计、配置与性能要求。",
         core="规定系统架构、探测器选型布置、报警响应时间与联动控制等技术指标。",
         impl="将于2026年9月1日正式实施，存量与新建储能电站需加快合规改造。",
         url="https://std.samr.gov.cn/gb/search/gbDetailed?id=3DBA2132857B0D16E06397BE0A0A8119"),
]

html_parts = []
html_parts.append(h2("本周趋势展望"))
for t, d in trends:
    html_parts.append(
        '<section style="margin-bottom:10px;padding:10px 14px;background:#fff;border-left:3px solid #4a90d9;'
        'border-radius:4px;"><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:4px;'
        'line-height:1.5;">\U0001F539 %s</div><div style="font-size:13px;color:#333;line-height:1.7;">%s</div></section>'
        % (t, d))

LEGEND = (
    '<section style="margin:24px 0 12px 0;padding:14px 16px;background:#f5f9ff;'
    'border-left:3px solid #4a90d9;border-radius:4px;">'
    '<div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:4px;">'
    '\U0001F4CC 信源分级说明 · Admiralty / NATO AJP-2.1</div>'
    '<div style="font-size:12px;color:#555;line-height:1.7;margin-bottom:10px;">'
    '本报告采用 OSINT 开源情报领域公认的 Admiralty 评级标准（北约 AJP-2.1）：'
    '每条内容以双字符评级标注，首字符评<strong>信源可靠性</strong>，次字符评<strong>信息可信度</strong>，'
    '如 B2 = 通常可靠信源 × 很可能属实。两维独立评估，互不绑定。</div>'
    '<div style="font-size:12px;color:#1f5fa8;font-weight:bold;margin-bottom:4px;">'
    '信源可靠性 Source Reliability（A–F）</div>'
    '<div style="font-size:13px;color:#333;line-height:2.1;">'
    '<span style="background:#6abf69;color:#fff;font-size:11px;padding:1px 6px;'
    'border-radius:3px;">A</span> 完全可靠 · 政府机构公告与官方平台正式发布文本'
    '（认监委、全国标准信息公共服务平台等）· SCI 顶刊顶会（Nature/Science 系列等）<br/>'
    '<span style="background:#4a90d9;color:#fff;font-size:11px;padding:1px 6px;'
    'border-radius:3px;">B</span> 通常可靠 · SCI 期刊 · IEEE/JPS/EST 等权威学术出版 · '
    '权威媒体（新浪财经、东方财富等）· 受政府委托标准组织的征求意见公告'
    '（中电联受国家标准委/国家能源局委托发布 GB/DL 征求意见函）<br/>'
    '<span style="background:#e67e22;color:#fff;font-size:11px;padding:1px 6px;'
    'border-radius:3px;">C</span> 相当可靠 · arXiv 预印本 · 专业开源社区 · '
    '企业官方发布 · 行业资讯 · 团体标准<br/>'
    '<span style="background:#9b59b6;color:#fff;font-size:11px;padding:1px 6px;'
    'border-radius:3px;">D/E</span> 通常不可靠 / 不可靠 · 行业博客 / 自媒体<br/>'
    '<span style="background:#95a5a6;color:#fff;font-size:11px;padding:1px 6px;'
    'border-radius:3px;">F</span> 无法判断 · 信源记录不足以评估（兜底档）'
    '</div>'
    '<div style="font-size:12px;color:#1f5fa8;font-weight:bold;margin:8px 0 4px;">'
    '信息可信度 Information Credibility（1–6）</div>'
    '<div style="font-size:13px;color:#333;line-height:2.1;">'
    '<b>1</b> 完全可信，已被独立信源证实&nbsp;&nbsp;'
    '<b>2</b> 很可能属实，可靠单源一手文本&nbsp;&nbsp;'
    '<b>3</b> 可能属实，单源转述待核&nbsp;&nbsp;'
    '<b>4</b> 存疑&nbsp;&nbsp;<b>5</b> 不可能&nbsp;&nbsp;<b>6</b> 真实性无法判断（兜底档）'
    '</div>'
    '<div style="font-size:12px;color:#888;line-height:1.7;margin-top:8px;">'
    '注：信源可靠性仅刻画信源先验，不等价于信息已被证实——高可靠信源亦可能刊发未经证实内容；'
    'D/E 及 4/5 档条目仅供参考，不构成投资建议。</div>'
    '</section>')
html_parts.append(LEGEND)

html_parts.append(h2("一、学术论文进展"))
for i, p in enumerate(papers, 1):
    html_parts.append(paper(i, p["tier"], p["date"], p["journal"], p["topic"],
                            p["title"], p["abstract"], p["innovation"], p["url"]))

html_parts.append(h2("二、厂商动态"))
for i, v in enumerate(vendors, 1):
    html_parts.append(vendor(i, v["tier"], v["date"], v["t1"], v["t2"],
                             v["title"], v["abstract"], v["url"]))

html_parts.append(h2("三、开源项目与数据集"))
for i, o in enumerate(oss, 1):
    html_parts.append(opensrc(i, o["date"], o["t1"], o["t2"], o["title"], o["abstract"], o["url"]))

html_parts.append(h2("四、专利技术"))
for i, p in enumerate(patents, 1):
    html_parts.append(patent(i, p.get("tier", "C2"), p["date"], p["t1"], p["t2"], p["title"], p["holder"],
                             p["abstract"], p["innovation"], p["url"]))

html_parts.append(h2("五、行业标准"))
for i, s in enumerate(standards, 1):
    html_parts.append(standard(i, s["tier"], s["date"], s["t1"], s["t2"], s["title"],
                               s["purpose"], s["core"], s["impl"], s["url"]))

html_parts.append(
    '<section style="background:#f5f5f5;border-radius:8px;padding:16px;margin-top:24px;text-align:center;">'
    '<div style="font-size:12px;color:#888;line-height:1.8;margin-bottom:8px;">'
    '事实核查声明：本期内容来源已按 Admiralty / NATO AJP-2.1 标准双维评级标注，D/E 级信源条目仅供参考，不构成投资建议。</div>'
    '<div style="font-size:14px;color:#4a90d9;font-weight:bold;">\U0001F50B BMS 算法追踪</div>'
    '<div style="font-size:11px;color:#aaa;margin-top:4px;">关注电池管理系统前沿 | 每周更新</div></section>')

content = "".join(html_parts)

with open("report.html", "w", encoding="utf-8") as f:
    f.write(content)

# ---- self check ----
import re
h2_count = content.count("<h2")
url_count = len(re.findall(r"https?://", content))
journal_badges = sum(content.count(">arXiv<") for _ in [0]) if False else content.count(">arXiv<")
doi_count = content.count("https://doi.org/")
arxiv_count = content.count("https://arxiv.org/abs/")
cjk = len(re.findall(r"[\u4e00-\u9fff]", content))
print(f"H2 sections: {h2_count}")
print(f"URLs: {url_count}")
print(f"arXiv badge rows: {journal_badges}")
print(f"DOI links: {doi_count}")
print(f"arXiv links: {arxiv_count}")
print(f"Chinese chars: {cjk}")
print(f"toutiao links: {content.count('toutiao')}")
print(f"<a> tags: {content.count('<a ')}")
print(f"legend present: {'信源分级说明' in content}")
print(f"rating badges A2={content.count('>A2<')} B2={content.count('>B2<')} "
      f"C2={content.count('>C2<')} C3={content.count('>C3<')} D3={content.count('>D3<')}")
print(f"cec DL/GB consultation items B2: "
      f"{content.count('征求意见')} notices total")
print(f"legacy T-badges remaining: {len(re.findall(r'>T[1-4]<', content))}")

# unicode corruption scan: rare CJK check
from collections import Counter
freq = Counter(re.findall(r"[\u4e00-\u9fff]", content))
rare = [c for c, n in freq.items() if n == 1]
print(f"rare (freq=1) CJK chars: {len(rare)}: {''.join(rare[:60])}")
