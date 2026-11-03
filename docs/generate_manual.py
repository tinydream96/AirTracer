import os
import qrcode
from PIL import Image
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_manual():
    docs_dir = "/Users/luo/DATA/CodeProjects/AI_Projects/AirTracer/docs"
    qr_dir = "/Users/luo/.gemini/antigravity-ide/brain/f676a223-7828-4d50-ae8e-1523637aeb1e/scratch"
    os.makedirs(qr_dir, exist_ok=True)

    # 1. 生成官网二维码
    web_qr = os.path.join(qr_dir, "web_qr.png")
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data("https://airtracer.us/")
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0f172a", back_color="white")
    img.save(web_qr)

    # 2. 微信二维码处理（裁剪或直接使用）
    wechat_qr_path = os.path.join(docs_dir, "wechat_qr.jpg")

    doc = Document()

    # 页面边距设为较适合包装内放置的标准尺寸 (A4, 边距 1.5cm 约 0.59 英寸)
    for section in doc.sections:
        section.top_margin = Inches(0.55)
        section.bottom_margin = Inches(0.55)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)

    # 配色方案 (AirTracer 科技感 Slate & Indigo 蓝)
    COLOR_PRIMARY = RGBColor(30, 58, 138)     # #1e3a8a 深邃蓝
    COLOR_SECONDARY = RGBColor(14, 116, 144)  # #0e7490 青蓝
    COLOR_TEXT = RGBColor(30, 41, 59)         # #1e293b 灰黑正文
    COLOR_MUTED = RGBColor(100, 116, 139)     # #64748b 次要文字
    COLOR_WARNING = RGBColor(180, 83, 9)      # #b45309 琥珀黄

    # 设置默认样式字体
    style = doc.styles['Normal']
    font = style.font
    font.name = 'PingFang SC'
    font.size = Pt(9.5)
    font.color.rgb = COLOR_TEXT

    def set_run_font(run, font_name="PingFang SC", size_pt=9.5, bold=False, color_rgb=COLOR_TEXT):
        run.font.name = font_name
        run.font.size = Pt(size_pt)
        run.bold = bold
        run.font.color.rgb = color_rgb
        rPr = run._element.get_or_add_rPr()
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:eastAsia="{font_name}" w:hAnsi="{font_name}"/>')
        rPr.append(rFonts)

    def add_header_banner():
        table = doc.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        cell_left = table.cell(0, 0)
        cell_right = table.cell(0, 1)
        cell_left.width = Inches(5.4)
        cell_right.width = Inches(1.5)

        for cell in (cell_left, cell_right):
            tcPr = cell._element.get_or_add_tcPr()
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F1F5F9"/>')
            tcPr.append(shd)
            borders = parse_xml(f'''
                <w:tcBorders {nsdecls("w")}>
                    <w:top w:val="none"/>
                    <w:left w:val="none"/>
                    <w:bottom w:val="single" w:sz="12" w:space="0" w:color="3B82F6"/>
                    <w:right w:val="none"/>
                </w:tcBorders>
            ''')
            tcPr.append(borders)

        # 左侧标题与网址
        p_title = cell_left.paragraphs[0]
        p_title.paragraph_format.space_before = Pt(2)
        p_title.paragraph_format.space_after = Pt(2)
        run_badge = p_title.add_run("🛰️ AirTracer 轨迹追踪系统\n")
        set_run_font(run_badge, size_pt=15, bold=True, color_rgb=COLOR_PRIMARY)

        run_sub = p_title.add_run("Infi Tag 专属新手使用与操作指南\n")
        set_run_font(run_sub, size_pt=11.5, bold=True, color_rgb=COLOR_SECONDARY)

        run_url = p_title.add_run("官方平台网址：https://airtracer.us/  |  支持手机/平板/电脑浏览器")
        set_run_font(run_url, size_pt=8.5, color_rgb=COLOR_MUTED)

        # 右侧放置官网二维码
        p_qr = cell_right.paragraphs[0]
        p_qr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_qr.paragraph_format.space_before = Pt(2)
        p_qr.paragraph_format.space_after = Pt(1)
        run_img = p_qr.add_run()
        run_img.add_picture(web_qr, width=Inches(1.05))
        p_qr_desc = cell_right.add_paragraph()
        p_qr_desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_qr_desc.paragraph_format.space_before = Pt(0)
        p_qr_desc.paragraph_format.space_after = Pt(2)
        run_desc = p_qr_desc.add_run("扫码直达官网")
        set_run_font(run_desc, size_pt=8, color_rgb=COLOR_MUTED)

    def add_section_title(title_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(9)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title_text)
        set_run_font(run, size_pt=11, bold=True, color_rgb=COLOR_PRIMARY)

    def add_bullet_point(label, content, space_after=1.5):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.18)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if label:
            run_lbl = p.add_run(f"• {label}：")
            set_run_font(run_lbl, size_pt=9, bold=True, color_rgb=COLOR_TEXT)
        else:
            run_lbl = p.add_run("• ")
            set_run_font(run_lbl, size_pt=9, bold=True, color_rgb=COLOR_TEXT)
        run_cnt = p.add_run(content)
        set_run_font(run_cnt, size_pt=9, color_rgb=COLOR_TEXT)

    def add_callout(title, text, is_warning=False):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        cell = table.cell(0, 0)
        cell.width = Inches(6.95)

        tcPr = cell._element.get_or_add_tcPr()
        fill_color = "FEF3C7" if is_warning else "EFF6FF"
        border_color = "F59E0B" if is_warning else "3B82F6"

        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
        tcPr.append(shd)
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="none"/>
                <w:left w:val="single" w:sz="20" w:space="0" w:color="{border_color}"/>
                <w:bottom w:val="none"/>
                <w:right w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15

        color = COLOR_WARNING if is_warning else COLOR_PRIMARY
        run_title = p.add_run(title + ("\n" if text else ""))
        set_run_font(run_title, size_pt=9, bold=True, color_rgb=color)

        if text:
            run_text = p.add_run(text)
            set_run_font(run_text, size_pt=8.5, color_rgb=COLOR_TEXT)
        
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(2)

    def add_contact_box():
        p_title = doc.add_paragraph()
        p_title.paragraph_format.space_before = Pt(10)
        p_title.paragraph_format.space_after = Pt(4)
        p_title.paragraph_format.keep_with_next = True
        run_t = p_title.add_run("📞 联系我们与售后支持")
        set_run_font(run_t, size_pt=11, bold=True, color_rgb=COLOR_PRIMARY)

        table = doc.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        cell_left = table.cell(0, 0)
        cell_right = table.cell(0, 1)
        cell_left.width = Inches(4.7)
        cell_right.width = Inches(2.25)

        for cell in (cell_left, cell_right):
            tcPr = cell._element.get_or_add_tcPr()
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8FAFC"/>')
            tcPr.append(shd)
            borders = parse_xml(f'''
                <w:tcBorders {nsdecls("w")}>
                    <w:top w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>
                    <w:left w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>
                    <w:bottom w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>
                    <w:right w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>
                </w:tcBorders>
            ''')
            tcPr.append(borders)

        # 左侧联系详情
        p_info = cell_left.paragraphs[0]
        p_info.paragraph_format.space_before = Pt(6)
        p_info.paragraph_format.space_after = Pt(3)
        p_info.paragraph_format.line_spacing = 1.25

        run_sub = p_info.add_run("如在使用过程中遇到任何疑问、或需要绑定设备：\n\n")
        set_run_font(run_sub, size_pt=9, color_rgb=COLOR_MUTED)

        run_em_icon = p_info.add_run("✉️ 官方邮箱：\n")
        set_run_font(run_em_icon, size_pt=9.5, bold=True, color_rgb=COLOR_TEXT)
        run_em = p_info.add_run("    AirtagTracer@gmail.com\n\n")
        set_run_font(run_em, size_pt=10, bold=True, color_rgb=COLOR_PRIMARY)

        run_wx_icon = p_info.add_run("💬 客服微信：\n")
        set_run_font(run_wx_icon, size_pt=9.5, bold=True, color_rgb=COLOR_TEXT)
        run_wx = p_info.add_run("    扫描右侧二维码添加技术支持（备注：InfiTag）\n    工作时间提供一对一专属答疑与协助。")
        set_run_font(run_wx, size_pt=8.5, color_rgb=COLOR_MUTED)

        # 右侧微信二维码
        p_qr = cell_right.paragraphs[0]
        p_qr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_qr.paragraph_format.space_before = Pt(6)
        p_qr.paragraph_format.space_after = Pt(2)

        if os.path.exists(wechat_qr_path):
            run_img = p_qr.add_run()
            run_img.add_picture(wechat_qr_path, width=Inches(1.4))
            p_qr_desc = cell_right.add_paragraph()
            p_qr_desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_qr_desc.paragraph_format.space_before = Pt(0)
            p_qr_desc.paragraph_format.space_after = Pt(4)
            run_desc = p_qr_desc.add_run("扫码添加微信客服")
            set_run_font(run_desc, size_pt=8, color_rgb=COLOR_MUTED)

    # --- 开始生成排版内容 ---
    add_header_banner()

    # 一、账号注册与设备绑定
    add_section_title("一、 账号注册与设备绑定")
    add_bullet_point("1. 打开官网并注册", "访问 https://airtracer.us/ 点击【注册】，填写 3~20 位用户名、邮箱及密码。注册成功后务必点击【下载凭证】妥善保存密码。")
    add_bullet_point("2. 最关键一步：联系管理员绑定设备", "注册完成后，请将您的【用户名】或【注册邮箱】发送给售后/管理员为您完成名下设备绑定。")
    add_callout(
        "⚠️ 重要提示：设备绑定生效说明",
        "管理员绑定完成后，请重新登录或刷新页面，名下 Infi Tag 即会自动呈现于地图与列表，无需手动配对。\n注：新设备首次上线若处于室内弱信号盲区，请等待数分钟待周围有苹果设备路过完成首次定位上报。",
        is_warning=True
    )

    # 二、查看与切换设备
    add_section_title("二、 如何查看与切换设备？")
    add_bullet_point("📱 手机端用户", "屏幕底部设有胶囊状设备卡片。名下有多台设备时左右滑动卡片，轻点选中目标设备即可在地图上自动定位聚焦，右上角同步弹出详情卡片。")
    add_bullet_point("💻 电脑端用户", "屏幕左侧设有设备列表栏，直接用鼠标点击设备名称即可完成聚焦与选中。")

    # 三、查询与显示历史轨迹
    add_section_title("三、 历史轨迹查询与交互解读")
    add_bullet_point("📅 打开日期选择", "选中设备后，点击右上角信息卡片上的【📅 日历长条栏】（默认加载当天轨迹）。")
    add_bullet_point("🟢🟡🔴 轨迹颜色含义", "绿色代表低速/停留，黄色代表中速行驶，红色代表高速行进。线条上附带流动箭头指示运动方向。")
    add_bullet_point("📍 轨迹详情点", "点击路线上半透明的红色轨迹圆点，可即时查看精确记录时间、行驶速度、经纬度及定位精度。")

    # 四、精准查询指定时间
    add_section_title("四、 精准查询“指定时间段”轨迹（步骤与诀窍）")
    add_bullet_point("第 1 步：点击日期栏", "点击右上角信息卡片中间的日期区间按钮，弹出时间选择面板。")
    add_bullet_point("第 2 步：识别小圆点", "仔细查看日历日期下方——【凡是标有小圆点的日期，才代表该天有采集到轨迹记录】！无小圆点表示该天设备未产生位置。")
    add_bullet_point("第 3 步：选定起止时分", "日历上依次点选开始和结束日期，顶部下拉框可精细选择时间（如 08:30 至 18:00）。")
    add_bullet_point("第 4 步：必须点击【确认】", "选好日期与时间后，必须点击弹窗右下角蓝色的【确认】按钮！不要直接点击外部空白关闭，否则查询不会下发。")

    # 五、常见排查
    add_section_title("五、 常见排查：为什么选好了时间，地图上没有轨迹线？")
    add_bullet_point("1. 遗漏点击确认", "在日历选好后随手点击了空白处关闭，导致新条件未触发拉取。")
    add_bullet_point("2. 设备处于静止状态", "Infi Tag 发生位移时才会绘制连续线条。若全天静止，仅记录原地停留点，不会生成长距离行车路线。")
    add_bullet_point("3. 所选日期无小圆点", "设备基于全球 FindMy 网络，若置于地下室等完全无苹果设备经过的盲区，期间将无位置数据。")
    add_bullet_point("4. 时间倒置或跨度过窄", "误将开始时间选晚于结束时间；或时间跨度仅选了 1~2 分钟，该区间内恰好未达上报周期。")

    # 六、客户端安装
    add_section_title("六、 手机客户端安装指南（推荐使用）")
    add_bullet_point("🤖 安卓手机用户", "访问官网首页点击【下载 Android APK】或扫描旁边二维码，下载并安装官方 App。")
    add_bullet_point("🍎 苹果用户（PWA 原生体验）", "用 Safari 浏览器打开官网 → 点击底部【分享图标 📤】→ 选择【添加到主屏幕】→ 点击右上角【添加】。无需 App Store，即可在手机桌面获得独立全屏的原生级 App 体验！")

    # 七、实用小技巧
    add_section_title("💡 实用操作小技巧")
    add_bullet_point("信息卡片重新唤出", "若误关闭右上角卡片，点击地图右上角出现的【ℹ️ 信息图标】随时重新展开。")
    add_bullet_point("实时测距", "点击右下角【📍 我的位置】，系统将在右上角卡片实时显示设备“距您 xxx 米/公里”。")
    add_bullet_point("切换底图", "点击右下角【🗺️ 图层按钮】，可自由切换高德地图、高德卫星、天地图及谷歌地图。")

    # 联系我们
    add_contact_box()

    docx_path = os.path.join(docs_dir, "AirTracer_InfiTag_用户手册.docx")
    doc.save(docx_path)
    print(f"DOCX 生成成功: {docx_path}")
    return docx_path

if __name__ == "__main__":
    create_manual()
