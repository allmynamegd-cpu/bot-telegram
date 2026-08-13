import logging
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Lệnh /cmd để chạy câu lệnh hệ thống (Ví dụ: /cmd dir hoặc /cmd ipconfig)
async def run_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy nội dung người dùng nhập sau lệnh /cmd
    args = context.args
    if not args:
        await update.message.reply_text("Vui lòng nhập câu lệnh. Ví dụ: /cmd dir")
        return
    
    # Ghép các từ lại thành một câu lệnh hoàn chỉnh
    command = " ".join(args)
    
    try:
        # Sử dụng subprocess để chạy lệnh trên Windows/Linux
        # shell=True cho phép chạy trực tiếp lệnh giống như gõ trong CMD
        result = subprocess.run(command, capture_output=True, text=True, shell=True, timeout=10)
        
        output = result.stdout if result.stdout else result.stderr
        
        # Nếu kết quả quá dài (Telegram giới hạn 4000 ký tự), hãy cắt ngắn bớt
        if len(output) > 4000:
            output = output[:4000] + "\n... (Kết quả quá dài đã bị cắt bớt)"
            
        if not output.strip():
            output = "Lệnh đã chạy thành công nhưng không trả về kết quả gì."
            
        await update.message.reply_text(f"💻 **Kết quả:**\n```\n{output}\n```", parse_mode="Markdown")
        
    except subprocess.TimeoutExpired:
        await update.message.reply_text("⚠️ Câu lệnh chạy quá thời gian chờ (Timeout)!")
    except Exception as e:
        await update.message.reply_text(f"❌ Lỗi khi thực thi: {str(e)}")

if __name__ == '__main__':
    # Thay 'YOUR_TELEGRAM_BOT_TOKEN' bằng token thật của bạn
    app = ApplicationBuilder().token("ENTER YOUR TOKEN HERE").build()

    app.add_handler(CommandHandler("cmd", run_command))

    print("Bot điều khiển hệ thống đang chạy...")
    app.run_polling()
