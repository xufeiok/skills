#!/usr/bin/env python3
"""
西悦云庭每周小红书文案生成 + 飞书推送
工作流：生成草稿 → 飞书发我确认 → 我确认后 → 发布到飞书文档

模式:
  --action preview  生成文案并发送飞书消息预览（默认）
  --action publish  将上次生成的草稿发布到飞书文档（我确认后执行）
"""
import json, os, sys, requests
from datetime import datetime, timedelta
from pathlib import Path

APP_ID = os.environ.get("FEISHU_APP_ID", "cli_a96305a3b97a1cd3")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")
FOLDER_TOKEN = "JX9Mf6eOSlVkygd2pRzc3VlGnLh"
USER_OPEN_ID = "ou_9a0caef46ae39a2e88f9a867583b5821"
DRAFT_DIR = Path(os.path.expanduser("~/.hermes/scripts/drafts"))
DRAFT_DIR.mkdir(parents=True, exist_ok=True)


def get_feishu_token():
    r = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": APP_ID, "app_secret": APP_SECRET}, timeout=15
    )
    return r.json()["tenant_access_token"]


def send_feishu_message(token, title, preview_text):
    """通过飞书API发送消息到我的飞书"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    content = {
        "config": {"wide_screen_mode": True},
        "header": {"title": {"tag": "plain_text", "content": f"📝 {title}"}, "template": "blue"},
        "elements": [
            {"tag": "markdown", "content": preview_text},
            {"tag": "hr"},
            {"tag": "markdown", "content": "**请确认以上文案内容**\n回复「确认发布」后，我会将完整文档推送到飞书公开文档中。"},
            {"tag": "action", "actions": [
                {"tag": "button", "text": {"tag": "plain_text", "content": "✅ 确认发布"},
                 "type": "primary", "value": {"action": "confirm_publish"}}
            ]}
        ]
    }
    
    r = requests.post(
        "https://open.feishu.cn/open-apis/im/v1/messages",
        params={"receive_id_type": "open_id"},
        json={
            "receive_id": USER_OPEN_ID,
            "msg_type": "interactive",
            "content": json.dumps(content, ensure_ascii=False)
        },
        headers=headers, timeout=15
    )
    return r.json()


def send_simple_message(token, text):
    """发送纯文本消息"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    r = requests.post(
        "https://open.feishu.cn/open-apis/im/v1/messages",
        params={"receive_id_type": "open_id"},
        json={
            "receive_id": USER_OPEN_ID,
            "msg_type": "text",
            "content": json.dumps({"text": text}, ensure_ascii=False)
        },
        headers=headers, timeout=15
    )
    return r.json()


# ===== 日期和节气 =====
today = datetime.now()
this_friday = today + timedelta(days=(4 - today.weekday()) % 7 or 7)
dates = [(this_friday + timedelta(days=i)).strftime("%m月%d日 %A") for i in range(7)]
date_range_str = f"{this_friday.strftime('%Y.%m.%d')}-{(this_friday + timedelta(days=6)).strftime('%m.%d')}"

def get_seasonal_tag():
    m, d = today.month, today.day
    if m == 5:
        if d <= 5: return "立夏"
        if d <= 20: return "小满"
        if d <= 31: return "初夏"
    if m == 6:
        if d <= 5: return "芒种"
        if d <= 21: return "夏至"
        return "盛夏"
    if m == 7:
        if d <= 6: return "小暑"
        return "盛夏"
    if m == 8:
        if d <= 7: return "立秋"
        if d <= 23: return "处暑"
    return ""

season_tag = get_seasonal_tag()

# ===== 项目价值角度 =====
VALUE_ANGLES = [
    "国企（双国企背书，兴城人居+益民集团，交付保障）",
    "现房（所见即所得，即买即住）",
    "公园（北侧代建城市公园，内外双园格局）",
    "双园（代建公园+内部园林，致澜景观设计）",
    "醇熟配套（光华新城核心，周边商圈环绕）",
    "学校汇聚（邻近多所优质学校，全龄教育）",
    "低密（约2.0容积率，约445户纯居社区）",
    "全能套四（约133㎡四房双套房，满足三代同堂）",
    "横厅（约50㎡巨幕横厅，约8.95米超大开间）",
    "健康森活（低密社区+内外双园+温江天然氧吧）",
    "青年平墅（建筑面积约133平米青年平墅，超大阳台）",
]

# ===== 每天角度组合 =====
daily_angles = [
    ("周五", "国企+醇熟配套", "周末看房邀请"),
    ("周六", "青年平墅+全能套四+横厅", "产品力"),
    ("周日", "公园+双园+健康森活", "居住环境"),
    ("周一", "低密+现房", "社区品质"),
    ("周二", season_tag + "季节生活场景", "季节情绪"),
    ("周三", "国企+学校汇聚", "信任+教育"),
    ("周四", "醇熟配套+青年平墅", "板块价值"),
]

# ===== 操作 =====
def action_preview():
    print(f"📅 本周文案周期: {date_range_str} (周五~下周四)")
    print(f"🌿 当前节气/季节: {season_tag or '无'}")
    print(f"📋 项目价值角度: {len(VALUE_ANGLES)}个")
    
    # 生成文案骨架（实际内容由 LLM 在 cron job 中填充）
    contents = []
    for i, (dow, angles, scene) in enumerate(daily_angles):
        date_str = dates[i]
        content_block = {
            "day": dow,
            "date": date_str,
            "angles": angles,
            "scene": scene,
            "title": "",
            "body": ""
        }
        contents.append(content_block)
    
    # 保存草稿供后续publish使用
    draft = {
        "date_range": date_range_str,
        "season_tag": season_tag,
        "generated_at": datetime.now().isoformat(),
        "status": "draft",
        "contents": contents,
        "value_angles": VALUE_ANGLES
    }
    draft_file = DRAFT_DIR / "latest_xhs_draft.json"
    draft_file.write_text(json.dumps(draft, ensure_ascii=False, indent=2))
    
    # 构建飞书预览消息
    preview_lines = [
        f"**周期**: {date_range_str}（周五~下周四）",
        f"**节气**: {season_tag or '无'}",
        f"**用途**: 西悦云庭置业顾问转发宣传",
        "",
        "**本周7天角度安排：**",
    ]
    for i, (dow, angles, scene) in enumerate(daily_angles):
        preview_lines.append(f"  **{dow}({dates[i]})**: {angles} — {scene}")
    
    preview_lines += [
        "",
        "**可调用项目价值角度：**",
        "、".join(VALUE_ANGLES),
        "",
        "**知识库参考：**",
        "详情见 /vol1/1000/KnowledgeBase/lib-地产/wiki/entities/西悦云庭.md",
    ]
    
    preview_text = "\n".join(preview_lines)
    
    # 发送飞书消息
    title = f"西悦云庭小红书文案-{date_range_str}"
    
    try:
        token = get_feishu_token()
        result = send_feishu_message(token, title, preview_text)
        print(f"\n✅ 飞书预览消息已发送！")
        print(f"   消息ID: {result.get('data', {}).get('message_id', 'unknown')}")
        print(f"\n⏳ 请查看飞书，确认文案内容后回复「确认发布」")
        print(f"   确认后我会执行:")
        print(f"   python weekly_xhs_plan.py --action publish")
    except Exception as e:
        print(f"⚠ 飞书消息发送失败: {e}")
        print(f"   但草稿已保存，可手动确认。")
    
    print(f"\n📄 草稿已保存: {draft_file}")
    print(f"📋 文档名: {title}")
    print(f"\nJSON_OUTPUT:{{\"title\":\"{title}\",\"draft_file\":\"{draft_file}\",\"date_range\":\"{date_range_str}\"}}")


def action_publish():
    """发布已确认的草稿到飞书文档"""
    draft_file = DRAFT_DIR / "latest_xhs_draft.json"
    if not draft_file.exists():
        print("❌ 没有找到草稿文件。请先生成预览。")
        sys.exit(1)
    
    draft = json.loads(draft_file.read_text())
    if draft["status"] == "published":
        print("⚠ 该草稿已发布过，如需重新发布请先生成新的草稿。")
        sys.exit(1)
    
    doc_title = f"西悦云庭销售小红书文案-{draft['date_range']}"
    print(f"📄 正在发布: {doc_title}")
    
    try:
        token = get_feishu_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        # 1. 创建文档
        cr = requests.post(
            "https://open.feishu.cn/open-apis/docx/v1/documents",
            json={"title": doc_title}, headers=headers, timeout=15
        )
        doc_data = cr.json()
        doc_token = doc_data.get("data", {}).get("document", {}).get("document_id", "")
        if not doc_token:
            print(f"❌ 创建文档失败: {doc_data}")
            sys.exit(1)
        print(f"✅ 文档已创建")
        
        # 2. 移动到文件夹
        requests.post(
            f"https://open.feishu.cn/open-apis/drive/v1/files/{doc_token}/move",
            json={"type": "file", "folder_token": FOLDER_TOKEN},
            headers=headers, timeout=15
        )
        print(f"📁 已移动到「西悦云庭销售小红书文案」文件夹")
        
        # 3. 写入内容（逐段）
        doc_lines = [
            f"# {doc_title}",
            "",
            f"🌿 周期：{draft['date_range']}（周五~下周四）",
            f"💡 用途：置业顾问转发宣传",
            "",
            "---",
        ]
        
        for item in draft["contents"]:
            doc_lines.append(f"## 📅 {item['date']}（{item['day']}）")
            doc_lines.append("")
            doc_lines.append(f"角度：{item['angles']}")
            doc_lines.append(f"场景：{item['scene']}")
            doc_lines.append("")
            if item["title"]:
                doc_lines.append(f"标题：{item['title']}")
            if item["body"]:
                doc_lines.append(f"正文：{item['body']}")
            doc_lines.append("")
            doc_lines.append("---")
            doc_lines.append("")
        
        for line in doc_lines:
            if not line.strip():
                continue
            block_type = 3
            if line.startswith("# ") or (line.startswith("#") and not line.startswith("##") and not line.startswith("###")) and len(line) < 50:
                block_type = 4
            elif line.startswith("## "):
                block_type = 5
            elif line.startswith("### "):
                block_type = 6
            elif line.startswith("---"):
                block_type = 22
            
            content_text = line.lstrip("# ").strip() if block_type > 3 else line
            requests.post(
                f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{doc_token}/children",
                json={"children": [{"block_type": block_type, "text": {
                    "elements": [{"text_run": {"content": content_text}}]
                }}]},
                headers=headers, timeout=15
            )
        
        # 4. 设置公开权限
        requests.patch(
            f"https://open.feishu.cn/open-apis/drive/v1/permissions/{doc_token}/public",
            json={
                "external_access_entity": "open",
                "security_entity": "anyone",
                "comment_entity": "anyone",
                "share_entity": "anyone",
                "link_share_entity": "anyone_readable"
            },
            headers=headers, timeout=15
        )
        
        doc_url = f"https://x0k1x5b6h3.feishu.cn/docx/{doc_token}"
        print(f"\n✅ 发布完成！")
        print(f"📄 文档: {doc_url}")
        print(f"📁 位置: 西悦云庭销售小红书文案/")
        
        # 更新草稿状态
        draft["status"] = "published"
        draft["published_url"] = doc_url
        draft["published_at"] = datetime.now().isoformat()
        draft_file.write_text(json.dumps(draft, ensure_ascii=False, indent=2))
        
        # 发送飞书通知
        try:
            send_simple_message(token, 
                f"✅ 西悦云庭小红书文案已发布！\n"
                f"📄 {doc_title}\n"
                f"🔗 {doc_url}\n"
                f"📁 位置：西悦云庭销售小红书文案文件夹")
        except:
            pass
        
        print(f"\nJSON_OUTPUT:{{\"url\":\"{doc_url}\",\"token\":\"{doc_token}\",\"title\":\"{doc_title}\"}}")
        
    except Exception as e:
        print(f"❌ 发布失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="西悦云庭每周小红书文案")
    parser.add_argument("--action", choices=["preview", "publish"], default="preview",
                        help="preview=生成预览并飞书发我确认(默认) | publish=确认后发布到飞书文档")
    args = parser.parse_args()
    
    if args.action == "publish":
        action_publish()
    else:
        action_preview()
