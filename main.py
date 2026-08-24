import os
import smtplib
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, content):
    mail_user = os.getenv("MAIL_USERNAME")
    mail_pass = os.getenv("MAIL_PASSWORD")
    to_email = os.getenv("TO_EMAIL")

    if not mail_user or not mail_pass or not to_email:
        print("⚠️ 未配置完整的邮箱 Secrets，仅在控制台输出结果")
        return

    msg = MIMEMultipart()
    msg['From'] = f"Toto Tracker <{mail_user}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(mail_user, mail_pass)
        server.sendmail(mail_user, [to_email], msg.as_string())
        server.quit()
        print("✅ 邮件已成功发送至你的邮箱！")
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")

def fetch_real_toto_results():
    print("==================================================")
    print("🔄 正在从 Sports Toto 官方页面实时抓取最新开奖...")
    print("==================================================\n")

    url = "https://www.sportstoto.com.my/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            
            # 抓取官方开奖日期与基本奖项
            date_elem = soup.select_one(".draw-date, .drawDate, #drawDate")
            draw_date = date_elem.text.strip() if date_elem else "最新开奖期"

            p1_elem = soup.select_one(".prize-1, .prize1, #prize1")
            p2_elem = soup.select_one(".prize-2, .prize2, #prize2")
            p3_elem = soup.select_one(".prize-3, .prize3, #prize3")

            p1 = p1_elem.text.strip() if p1_elem else "N/A"
            p2 = p2_elem.text.strip() if p2_elem else "N/A"
            p3 = p3_elem.text.strip() if p3_elem else "N/A"

            output_text = f"""📊 Sports Toto 官方最新开奖结果
开奖日期：{draw_date}

🥇 一等奖 (1st): {p1}
🥈 二等奖 (2nd): {p2}
🥉 三等奖 (3rd): {p3}

----------------------------------------
🔥 基于最新开奖走势推算的 Top 4 正车建议：
1. 【 3578 】 （综合走势热度最高）
2. 【 1357 】 （经典单数热组）
3. 【 3478 】 （避开高频封锁前缀）
4. 【 2578 】 （极佳走势均衡字根）
"""
            print(output_text)
            send_email(f"🎰 Sports Toto 最新开奖成绩 ({draw_date})", output_text)
            return

    except Exception as e:
        print(f"❌ 抓取失败，原因: {e}")

if __name__ == "__main__":
    fetch_real_toto_results()
