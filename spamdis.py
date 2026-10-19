import os
import aiohttp
import asyncio
import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput

# Danh sách câu spam / ngôn gốc
MESSAGES = [
    "sao m rụng ngay khi anh đến r",
    "mồ côi thắp hương cha mẹ trc khi chửi chưa",
    "mồ côi không cha mẹ đổ thừa cay bố m kìa",
    "‎‎tao thánh chửi mà :))‎‎",  
    "tây tạng béo mỡ cha chọc chết tươi rồi😹",
    "m còn trò j thể hiện nhanh lên ơ kìa",
    "óc chó ko trình lên đây sủa mạnh mẽ lên anh chơi mày cả ngày mà😹",
    "ơ hay óc chó ơi m sủa mạnh mẽ lên sao lại bị dập rồi",
    "lêu lêu thằng ngu không làm gì được cay anh kìa",
    "haha óc chó gà bị chửi cay cú ớt mẹ rồi: )))",
    "óc chó ngu nghèo cay cha bán mạng đi chửi cha má kìa: ))))",
    "m chạy đâu v con chó ngu ơi không được chạy mà: (((",
    "ai đụng gì óc chó để nó sợ rồi chạy thục mạng kìa",
    "culi ngu bị anh chửi té tát nước vô mặt m kìa: )))",
    "culi bị chửi mất xác kìa😹😹😹",
    "thằng nguuu giết cha bóp cổ má để cầu win anh à 😏 👉",
    "hi vọng làm dân war của con ngu bị t dập tắt từ khi nó sủa điên trước mặt t ae=)))",  
    "bà nội m loạn luân vs bố m còn ông ngoại m loạn luân vs mẹ m mà thg não cún =)) 🤪",
    "Cn thú mại dâm bán dâm mà như bán trinh hoa hậu v🤣",
    "con ngu nứng quá đến cả con mom nó gần u60 r nó vẫn ko tha=))",
    "Mẹ mày làm con chó canh cửa cho nhà t mà🤣",  
    "đáp ngôn nhanh hơn tý đc k tk ngu xuẩn🌬 🤢🤢",
    "bắt quả tang con chó chạy bố nè",
    "não cún chỉ biết âm thầm seen và ôm gối khóc mà huhuh 👈😜",
    "‎‎ con cave này adr 16gb đg kiếm tiền mua ip đk🤣🤣",
    " Vào 1 hôm bỗng con đĩ mẹ nhà m die thì lúc đó cha làm bá chủ sàn mẹ r :))",
    "‎con đĩ mẹ mày bất lực vì bị tao chửi mà chỉ biết câm lặng:))",
    "mẹ mày bị t đụ đột quỵ ngoài nhà nghỉ kìa đem hòm ra nha",
    "đem hai cái mày với con mẹ m luôn nha",
    "‎‎thời gian trôi qua để cảm nhận nỗi đau đi ửa à",
    "‎‎ nhai t chặt đầu con đĩ má m ra đó",
    "thằng ngu lgbt da đen sủa lẹ ai cko mày câm",
    "thằng sex thú đang cố làm cha cay hả thằng bại não",
    "tao miễn nhiễm mà thằng ngu",
    "Anh Bá Vcl Lỡ Đá Chết Mẹ mày Rồi  😝 👎",
    "Mẹ Mày Bị Cha Đụ Từ Nam Vào Đến Bắc Mà 🤪 👊",
    "Mẹ Mày Banh Háng Cho Khách Đụ Kìa Thằng Óc",
    "Tao Lỡ Cho Mẹ Mày Bú Cu Tao Rồi Sướng Vãi Cặc🧐 🤙",
    "Lêu Lêu Nhìn Cha Đụ Mẹ Mày Ko Làm Được Gì À Đừng Có Cay Cha Nha 😝 👎",
    "‎‎bị tao khủng bố quá nát mẹ cái hộp sọ với não luôn rồi à =))",
    "m là con đĩ đầu đinh giết má để loạn luân với bố mà con khốn",
    "văn thơ anh lai láng để con mẹ m dạng háng mỗi đêm =)))",
    "qua sông thì phải bắc cầu kiều con mẹ mày muốn làm đĩ phải yêu chiều các anh mà 🤣👈",
    "con lồn ngu này hay đạp xe đạp ngang nhà tao bị tao chọi đá về méc mẹ mà🤣",
    "thằng ngu này đang đi bộ bị t đánh úp nó về mách mẹ mà ae 🤣🤣",
    "thằng này ăn và khen chubin anh singu khen ngon quá=))",
    "thằng đầu đinh ở nhà lá mà ae nó mơ ước dc ở biệt thự như tui:))",
    "cả họ nhà mày phải xếp hàng lần lượt bú dái t mà🤣🤣",
    "thằng ảo war bị tao chửi cố gắng phản kháng nhưng nút home k cho phép mày cay quá đập cmn máy 🤣👈",
    "Sống như 1 con chó ngu dốt như lũ phèn ói chợ búa cầm dao múa kiếm",
    "Cha mày hóa thân thành hắc bạch vô thường cha mày bắt hồn đĩ mẹ mày xuống chầu diêm vương",
    "Nghèo bần hèn bị cha mày đứng trên đạp đầu lũ đú chúng mày cha đi lên",
    "Đú má mày tới tháng xịt nước máu kinh cho thk cha mày uống",
    "mày đi học bị bạn bè chê xài nút home mày cay quá về đánh đập bà già kiu bả làm đĩ để có tiền mua dt mới đi sĩ với bạn bè =))",
    "Con điếm phò mã bị cha mày cầm cái cây chà bồn cầu cha chà nát lồn mày nè",
    "Đừng có lên mạng xã hội tạo nét mà bị anh hành là mếu máo đi cầu cứu ngay",
    "mày thấy anh chửi thấm quá và nghĩ trong đầu là : anh này bá vcl đéo chửi lại nó đâu:)))",
    "thằng này đang ăn bị t đứng trên nóc nhà nó t ỉa trúng bát cơm nó luôn mà ae",
    "mày bí ngôn tới nỗi phải lên gg ghi : những câu chửi nhau hay nhất để phản kháng tao mà🤣👈",
    "mày thấy a chửi hay quá nên xin làm đệ của anh để được kéo làm hw:)))",
    "mày bị chửi tới nỗi tăng huyết áp phải cầu xin anh tha thứ:)))",
    "người yêu nó bị t đụ rên ư ử khen ku a  to và dài thế:))))",
    "mẹ nó khen cặk t to chấp nhận bỏ ba nó vì ông ấy ysl:)))",
    "cha nó ôm hận t lắm chỉ biết đứng ôm cặk khóc trong vô vọng:)))",
    "mẹ nó bị t đụ chán chê xong bị t trap t yêu người mẫu mà 🤣👈",
    "con bướm trâu bị gái có cu yêu qua mạng trap=)))Gbao w kayros",
    "trăng kia ai vẽ mà tròn loz con mẹ m bị ai địt mà mòn 1 bên 🤣",
    "mẹ m có phải còn búp bê tình dục để a lục đục mỗi đêm k 😏?",
    "mẹ m thì xóc lọ cho t còn người ta thì kính lão đắc thọ",
    "m tin bố lấy yamaha bố đề số 3 bố tông vào loz cn đĩ mẹ m k",
    "m gặp các anh đây toàn đấng tối cao a cầm con dao a đâm a thọc a chọc vào cái lỗ loz cn mẹ m mà 🤣👈",
    "cha m lấy gạch ống chọi nát cái đầu mu lồn mẹ mày giờ con bẻm đú",
    "con mồ côi mày mà rớt là tao lấy chiếc xe rùa t cán lòi mu lồn mẹ m đó gán trụ nha",
    "cú đấm sấm sét của anh mtrung đấm nát cái lồn mẹ thằng chó đú nhây như mày🤣👈",
    "cú đá cuồng phong đá bung cái lồn mẹ mày nè thằng não cặc🤣👈",
    "anh lấy cái ô tô anh đâm thẳng dô cái lồn con gái mẹ thằng súc vật như m",
    "hôm nay anh sẽ thay trời hành đạo anh cạo nát cái lông lồn con gái mẹ mày đó nghe chưa",
    "anh đẹp trai hai mái quay qua bên trái đái nát dô cái bàn thờ gái mẹ nghe hong con dog=))",
    "con đĩ eo di bi ti bị mẹ mày hành cho tới đột quỵ k có tiền lo t//ang lễ phải quỳ qua háng tao van xin tao cho tiền đúng kh",
    "thằng cặc chứng kiến cái cảnh mẹ nó bị t cầm bật lửa đốt từng cộng lông bướm:)))",
    "Anh gõ chết con đĩ mẹ mày giờ mày sủa ngôn có st tý coi em nhìn em phèn dạ anh mày chửi luôn ông bà mày đái lên mặt mày nhé con sút vật yếu kém",
    "thằng óc cặc bị tao ném xuống ao nhưng béo quá bị chết chìm🐕",
    "mày bị tao hành hung cho sắp đột tử rồi kìa kêu con đĩ mẹ mày qua cứu vãn mày lẹ đi không là tao cho mày nằm quan tài gào khóc thảm thiết trong đó liền ngay 3s nè con đĩ phế",
    "nhanh lên con chó lồn khai khắm=))",
    "con gái mẹ mày die dưới tay bọn anh kìa",
    "thằng bẻm bị t thọc cặc lên ổ cứng phát não rớt ra ngoài=)))",
    "cạn bã của XH mà tưởng mình hay hã con thú🤣💨",
    "thằng óc dái khi nghe tin cha nó chết kiểu: úi úi thằng già này cuối cùng cũng chết r vui vl=))",
    "thằng lồn ảo anime bật gear 5 lên địt con già nó trước bàn thờ tổ tiên=))",
    "anh cha dượng của bọn mày mà tụi bú cứt 🤣",
    "đây là suy nghĩ của con ngu sau khi nó bị tao sỉ nhục trong đầu nó bây giờ kiểu: quân tử trả thù 10 năm chưa muộn :)))))",
    "thằng ngu bị tao áp đảo từ phút 1 tới giờ nó k có cơ hội để sủa luôn ae=)))",
    "thằng đú bot mời ae nó sang nhà đụ bà già nó free vì hôm nay là ngày vui vì cha nó mới qua đời=))",
    "thằng cặc bị tao hạ đo ván sau 1 cú sút ngoạn mục đến từ vị trí anh trung hw=)))",
    "thằng óc cặc đòi va anh và cái kết bị anh chửi chạy khắp nơi=))",
    "mẹ mày bị tao địt rách màn trinh mà🤪",
    "🤭🤭Mày bê đê ngũ sắc dell công khai bị tao chọc quá máu cặc mày dồn lên não choa mày chết hả",
    "nhà thằng đú này nghèo không có tiền chơi gái nên phải loạn luân luôn với mẹ nó để giải khát cơn thèm thuồng",
    "thằng cầm thú loạn luân some với mẹ ruột và ba ruột còn quay clip",
    "m bị óc cứt hay sao z hả mà t nói m dell hiểu hay bố phải nhét cứt vào đầu m thì m mới thông hả con óc lồn ơi",
    "Một lũ xam cu lên đây đú ửa ngôn thì nhạt như cái nước lồn của con đỉ mẹ cm v hăng lên đi con mẹ mày bị t xé rách mu sao chối ????",
    "bà già mày bị tao treo cổ lên trên trần nhà mà?",
    "thằng bất tài vô dụng sủa mạnh lên đi",
    "cố gắng để win tao nhá",
    "tao bất bại mà thằng ngu?",
    "mẹ mày bị t đầu độc đến chết mà",
    "mày đàn ông hay đàn bà yếu đuối vậy",
    "con chó đầu đinh bị anh cầm cái đinh ba a thọc vào lỗ nhị nó mà ae =))",
    "thằng như mày xứng đáng ăn cứt tao á",
    "Mấy Con Thú Sài Tool Cha Đòi Bem Cha À",
    "Nghe Cha Chửi Con Gái Mẹ Mày Nè Con Ngu",
    "Mẹ Mày Bị Tao Lấy Phóng Lợn Chọt Dô Mu Lồn Khi Đang Đi Làm Gái Ở Ngã 3 Trần Duy Hưng🤣👈",
    "con mẹ m nghe tin m loạn luân vs bố m nên lấy dao cắt cổ tự tử r kìa con ngu :))",
    "m tìm câu nào sát thương tí được k thằng nghịch tử đâm bố đụ mẹ :)) 🤣",
    "óc chó bị anh chửi nhớ cha nhớ mẹ nhớ kiếp trước kìa😹😹😹"
]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

active_spam_tasks = []
active_vc_tasks = []

# ---------------------------------------------------------
# Tiến trình Spam
# ---------------------------------------------------------
async def run_spam_task(tokens, channels, mention_ids, delay):
    headers_list = [{"Authorization": t.strip(), "Content-Type": "application/json"} for t in tokens if t.strip()]
    channel_list = [c.strip() for c in channels if c.strip()]
    if not headers_list or not channel_list:
        return
    mention_text = " ".join([f"<@{uid}>" for uid in mention_ids]) if mention_ids else ""
    semaphore = asyncio.Semaphore(5)
    try:
        async with aiohttp.ClientSession() as session:
            while True:
                for msg in MESSAGES:
                    for idx, headers in enumerate(headers_list):
                        channel_id = channel_list[idx % len(channel_list)]
                        typing_url = f"https://discord.com/api/v10/channels/{channel_id}/typing"
                        send_url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
                        try:
                            async with semaphore:
                                await session.post(typing_url, headers=headers)
                                await asyncio.sleep(delay)
                                full_msg = f"{mention_text} {msg}" if mention_text else msg
                                async with session.post(send_url, json={"content": full_msg}, headers=headers) as resp:
                                    pass
                        except Exception:
                            pass
                    await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        pass

# ---------------------------------------------------------
# Tiến trình Treo Room Vĩnh Viễn (Có cơ chế Auto-Reconnect)
# ---------------------------------------------------------
async def keep_alive_voice(token, channel_id):
    ws_url = "wss://gateway.discord.gg/?v=10&encoding=json"
    headers = {"Authorization": token.strip(), "Content-Type": "application/json"}
    
    while True:
        guild_id = None
        async with aiohttp.ClientSession() as session:
            # 1. Tự động lấy Server ID từ Channel ID
            try:
                async with session.get(f"https://discord.com/api/v10/channels/{channel_id}", headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        guild_id = data.get("guild_id")
            except Exception:
                pass
                
            if not guild_id:
                await asyncio.sleep(10)
                continue

            # 2. Kết nối WebSocket Gateway duy trì 24/24 vĩnh viễn
            try:
                async with session.ws_connect(ws_url) as ws:
                    identify_payload = {
                        "op": 2,
                        "d": {
                            "token": token,
                            "capabilities": 509,
                            "properties": {"os": "Android", "browser": "Discord Android", "device": "Android"}
                        }
                    }
                    await ws.send_json(identify_payload)
                    
                    voice_state_payload = {
                        "op": 4,
                        "d": {"guild_id": guild_id, "channel_id": channel_id, "self_mute": True, "self_deaf": True}
                    }
                    await ws.send_json(voice_state_payload)
                    
                    heartbeat_interval = 20.0
                    
                    # Lắng nghe phản hồi để lấy interval chuẩn từ Discord nếu có
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            data = msg.json()
                            if data.get("op") == 10:
                                heartbeat_interval = data["d"].get("heartbeat_interval", 20000) / 1000.0
                                
                        # Gửi gói tin heartbeat định kỳ liên tục không ngừng nghỉ
                        async def heartbeat_loop():
                            while True:
                                await asyncio.sleep(heartbeat_interval)
                                await ws.send_json({"op": 1, "d": None})
                                
                        hb_task = asyncio.create_task(heartbeat_loop())
                        
                        # Giữ kết nối, nếu sập sẽ thoát vòng lặp và tự kết nối lại ngay lập tức
                        while not ws.closed:
                            await asyncio.sleep(1)
                        hb_task.cancel()
                        break
            except asyncio.CancelledError:
                break # Thoát hẳn nếu nhận lệnh stoprom
            except Exception:
                pass
        
        # Chờ 3 giây rồi tự động kết nối lại nếu bị rớt mạng
        await asyncio.sleep(3)

async def run_vc_task(tokens, channel_id):
    for token in tokens:
        task = asyncio.create_task(keep_alive_voice(token.strip(), channel_id))
        active_vc_tasks.append(task)

# ---------------------------------------------------------
# Modal Spam
# ---------------------------------------------------------
class SpamModal(Modal, title="Cấu hình Spam Discord"):
    tokens_input = TextInput(label="Token (Ngăn cách bằng dấu phẩy)", style=discord.TextStyle.paragraph, placeholder="token1, token2...", required=True)
    channels_input = TextInput(label="ID Kênh (Ngăn cách bằng dấu phẩy)", style=discord.TextStyle.short, placeholder="id_kenh_1, id_kenh_2...", required=True)
    tags_input = TextInput(label="ID Tag (Để trống nếu không tag)", style=discord.TextStyle.short, required=False)
    delay_input = TextInput(label="Delay giả typing (giây)", style=discord.TextStyle.short, default="1.0", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        tokens = [t.strip() for t in self.tokens_input.value.split(",") if t.strip()]
        channels = [c.strip() for c in self.channels_input.value.split(",") if c.strip()]
        mention_ids = [m.strip() for m in self.tags_input.value.split(",") if m.strip()]
        try:
            delay = float(self.delay_input.value.strip())
        except ValueError:
            delay = 1.0

        await interaction.response.send_message("⚡ **Đã kích hoạt Spam thành công! Gõ !stopsp để dừng.**", ephemeral=True)
        task = asyncio.create_task(run_spam_task(tokens, channels, mention_ids, delay))
        active_spam_tasks.append(task)

# ---------------------------------------------------------
# Modal Treo Room (Chỉ cần nhập ID Phòng Voice)
# ---------------------------------------------------------
class VoiceModal(Modal, title="Cấu hình Treo Room Voice 24/7"):
    tokens_input = TextInput(label="Token tài khoản (Ngăn cách bằng dấu phẩy)", style=discord.TextStyle.paragraph, placeholder="token1, token2...", required=True)
    channel_id_input = TextInput(label="ID Phòng Voice", style=discord.TextStyle.short, placeholder="Nhập ID Phòng Voice...", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        tokens = [t.strip() for t in self.tokens_input.value.split(",") if t.strip()]
        channel_id = self.channel_id_input.value.strip()

        await interaction.response.send_message(f"🎧 **Đã kích hoạt treo room vĩnh viễn 24/24 cho {len(tokens)} tài khoản! Gõ !stoprom để dừng.**", ephemeral=True)
        await run_vc_task(tokens, channel_id)

# ---------------------------------------------------------
# Persistent View
# ---------------------------------------------------------
class MenuView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🚀 Cấu Hình & Chạy Spam", style=discord.ButtonStyle.green, custom_id="btn_spam_persistent")
    async def spam_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(SpamModal())

    @discord.ui.button(label="🎧 Cấu Hình & Treo Room", style=discord.ButtonStyle.blurple, custom_id="btn_voice_persistent")
    async def voice_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(VoiceModal())

# ---------------------------------------------------------
# Lệnh Bot
# ---------------------------------------------------------
@bot.event
async def on_ready():
    bot.add_view(MenuView())
    print(f"=== Bot [Trần Minh Đức] đã sẵn sàng dưới tên {bot.user} ===")

@bot.command(name="menu")
async def menu_command(ctx):
    embed = discord.Embed(
        title="🌊 TOOL QUẢN LÝ DISCORD BY TRẦN MINH ĐỨC 🌊",
        description=(
            "```yaml\n"
            "==========================================\n"
            "             ⚡ SYSTEM AEV10 ⚡           \n"
            "==========================================\n"
            "```\n"
            "│ ➤ **Developer**: Trần Minh Đức\n"
            "│ ➤ **Hệ thống**: Treo Vĩnh Viễn 24/24\n"
            "└────────────────────────────────────────────"
        ),
        color=discord.Color.purple()
    )
    embed.add_field(
        name="📘 Hướng dẫn sử dụng",
        value=(
            "• Bấm nút **🚀 Cấu Hình & Chạy Spam** để nhập thông tin spam.\n"
            "• Bấm nút **🎧 Cấu Hình & Treo Room** để treo voice vĩnh viễn (Chỉ cần ID Phòng Voice).\n"
            "• Lệnh dừng spam: `!stopsp`\n"
            "• Lệnh dừng treo room: `!stoprom`"
        ),
        inline=False
    )
    await ctx.send(embed=embed, view=MenuView())

@bot.command(name="stopsp")
async def stop_spam(ctx):
    global active_spam_tasks
    if not active_spam_tasks:
        await ctx.send("⚠️ Không có tiến trình spam nào đang chạy!")
        return
    count = len(active_spam_tasks)
    for task in active_spam_tasks:
        task.cancel()
    active_spam_tasks.clear()
    await ctx.send(f"🛑 **Đã dừng thành công {count} tiến trình Spam!**")

@bot.command(name="stoprom")
async def stop_room(ctx):
    global active_vc_tasks
    if not active_vc_tasks:
        await ctx.send("⚠️ Không có tài khoản nào đang treo room!")
        return
    count = len(active_vc_tasks)
    for task in active_vc_tasks:
        task.cancel()
    active_vc_tasks.clear()
    await ctx.send(f"🛑 **Đã ngắt kết nối và dừng treo room cho {count} tài khoản!**")
