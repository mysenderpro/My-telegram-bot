from telethon import TelegramClient, events

# بيانات الاتصال
API_ID = 31042869
API_HASH = 'dde8d708584c993abe1289242f9f5b58'

# الكلمات المفتاحية المعتمدة
KEYWORDS = [
    'ابي احد يسوي', 'ابغى احد يسوي', 'يسويلي', 'احتاج احد يسوي', 
    'اللي يعرف يسوي', 'ابي خصوصي', 'ابي معلمة', 'ابي قناة تشرح', 
    'تقرير التدريب', 'يشرح', 'ابغى خصوصي', 'ابغى خصوصيه', 
    'ابغى معلمات', 'ابغى معلمة', 'ابغى شرح مادة', 'مين افضل خصوصي', 
    'خصوصي', 'تقارير التدريبي', 'التقرير الشهري', 'التقرير الاسبوعي', 
    'التقرير النهائي', 'مختص', 'ابي يحل', 'ابي يسوي', 'يسوي', 
    'عندي بحث', 'عندي واجب', 'قناة تشرح'
]

# المجموعات المعتمدة فقط (العامة والخاصة)
SOURCE_GROUPS = [
    'TVTC_Management', 'TVTC_C', 'TVTC_20', 'kingsaud00', 'KFU2022i', 
    'appliedstudiesTaifUniversity', 'GD642221', 'G_TaibahuD', 
    'CooperativeTraining2', 'BusinessTR', 'UPM46', 'jaz_phz', 
    'Hail2005', 't4u_ii', 'SallaMerchants',
    'https://t.me/+Slp9Pteqrj1urxWs', 
    'https://t.me/+Ors-TYfzoKRkNzk0', 
    'https://t.me/+Ve6ntslvdkdmMzVk'
]

# المجموعة المستهدفة لاستلام النتائج
TARGET_GROUP = 'https://t.me/+-nB9sLCgG0JmOTZk'

# بدء الجلسة
client = TelegramClient('final_verified_session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_GROUPS))
async def handler(event):
    try:
        message_text = event.text if event.text else ""
        if any(word in message_text for word in KEYWORDS):
            chat = await event.get_chat()
            sender = await event.get_sender()
            
            # رابط يوزر المرسل
            sender_link = f"tg://user?id={sender.id}"
            if getattr(sender, 'username', None):
                sender_link = f"https://t.me/{sender.username}"
            
            # رابط المجموعة
            group_link = f"https://t.me/{chat.username}" if getattr(chat, 'username', None) else "مجموعة خاصة"
            
            # رابط الرسالة المباشر
            msg_id = event.id
            if getattr(chat, 'username', None):
                message_url = f"https://t.me/{chat.username}/{msg_id}"
            else:
                clean_id = str(chat.id).replace("-100", "")
                message_url = f"https://t.me/c/{clean_id}/{msg_id}"

            # تنسيق الرسالة
            header = f"🎯 **رسالة مطابقة جديدة**\n\n"
            header += f"👤 **المرسل:** [{getattr(sender, 'first_name', 'مجهول')}]({sender_link})\n"
            header += f"📢 **المجموعة:** [{chat.title}]({group_link})\n"
            header += f"🔗 **رابط الرسالة:** [اضغط هنا للانتقال]({message_url})\n"
            header += "--------------------------\n\n"

            await client.send_message(TARGET_GROUP, header + message_text, file=event.media, link_preview=False)
            print(f"✅ تم نقل رسالة من: {chat.title}")
            
    except Exception as e:
        print(f"❌ خطأ: {e}")

print("🚀 البوت يعمل الآن على المجموعات المعتمدة...")
client.start()
client.run_until_disconnected()
