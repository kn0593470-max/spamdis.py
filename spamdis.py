import os
import aiohttp
import asyncio
import time
import itertools
import discord
from discord.ext import commands
from discord.ui import View, Select, Modal, TextInput

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
    "qua sông thì phải bắc cầu kiều con mẹ mày muốn làm đĩ thì phải yêu chiều các anh mà 🤣👈",
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
    "Nghe Cha Chửi Chết Con Gái Mẹ Mày Nè Con Ngu",
    "Mẹ Mày Bị Tao Lấy Phóng Lợn Chọt Dô Mu Lồn Khi Đang Đi Làm Gái Ở Ngã 3 Trần Duy Hưng🤣👈",
    "con mẹ m nghe tin m loạn luân vs bố m nên lấy dao cắt cổ tự tử r kìa con ngu :))",
    "m tìm câu nào sát thương tí được k thằng nghịch tử đâm bố đụ mẹ :)) 🤣",
    "óc chó bị anh chửi nhớ cha nhớ mẹ nhớ kiếp trước kìa😹😹😹"
]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# ---------------------------------------------------------
# 1. Tác vụ chạy Spam ngầm
# ---------------------------------------------------------
async def run_spam_task(tokens, channels, mention_ids, delay):
    headers_list = [{"Authorization": t.strip(), "Content-Type": "application/json"} for t in tokens if t.strip()]
    channel_list = [c.strip() for c in channels if c.strip()]
    if not headers_list or not channel_list:
        return
    mention_text = " ".join([f"<@{uid}>" for uid in mention_ids]) if mention_ids else ""
    semaphore = asyncio.Semaphore(5)
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

# ---------------------------------------------------------
# 2. Tác vụ Treo Room Voice 24/7 (Sử dụng discord.py client phụ để join voice)
# ---------------------------------------------------------
async def run_vc_task(tokens, invite_url):
    # Lấy invite code từ link (vd: https://discord.gg/z3J3JvNuE -> z3J3JvNuE)
    invite_code = invite_url.split("/")[-1].strip()
    
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        
        # Tạo một bot client riêng cho từng token phụ (self-bot/userbot cắm voice)
        sub_client = commands.Bot(command_prefix="!", intents=discord.Intents.default())
        
        @sub_client.event
        async def on_ready():
            try:
                invite = await sub_client.fetch_invite(invite_code)
                if invite and invite.voice_channel:
                    channel = invite.voice_channel
                    # Kết nối vào voice channel và giữ kết nối 24/7
                    if not sub_client.voice_clients:
                        vc = await channel.connect(self_deaf=True, self_mute=True)
                        print(f"[{sub_client.user}] Đã treo thành công vào Voice Room: {channel.name}")
            except Exception as e:
                print(f"Lỗi treo room token {token[:10]}...: {e}")

        # Chạy ngầm client phụ dưới dạng task độc lập
        asyncio.create_task(sub_client.start(token, bot=False))

# ---------------------------------------------------------
# 3. Bảng Modal nhập liệu cho Spam
# ---------------------------------------------------------
class SpamModal(Modal):
    def __init__(self):
        super().__init__(title="Cấu hình Spam Discord")
        self.tokens_input = TextInput(label="Token (Nhiều token ngăn cách dấu phẩy)", style=discord.TextStyle.paragraph, placeholder="token1, token2...", required=True)
        self.channels_input = TextInput(label="ID Kênh (Nhiều ID ngăn cách dấu phẩy)", style=discord.TextStyle.short, placeholder="id_kenh_1, id_kenh_2...", required=True)
        self.tags_input = TextInput(label="ID Tag (Để trống nếu không tag)", style=discord.TextStyle.short, required=False)
        self.delay_input = TextInput(label="Delay giả typing (giây)", style=discord.TextStyle.short, default="1.0", required=True)
        self.add_item(self.tokens_input)
        self.add_item(self.channels_input)
        self.add_item(self.tags_input)
        self.add_item(self.delay_input)

    async def on_submit(self, interaction: discord.Interaction):
        tokens = [t.strip() for t in self.tokens_input.value.split(",") if t.strip()]
        channels = [c.strip() for c in self.channels_input.value.split(",") if c.strip()]
        mention_ids = [m.strip() for m in self.tags_input.value.split(",") if m.strip()]
        try:
            delay = float(self.delay_input.value.strip())
        except ValueError:
            delay = 1.0

        await interaction.response.send_message("⚡ **Đã kích hoạt Spam Discord thành công!**", ephemeral=True)
        asyncio.create_task(run_spam_task(tokens, channels, mention_ids, delay))

# ---------------------------------------------------------
# 4. Bảng Modal nhập liệu cho Treo Room
# ---------------------------------------------------------
class VoiceModal(Modal):
    def __init__(self):
        super().__init__(title="Cấu hình Treo Room Voice 24/7")
        self.tokens_input = TextInput(label="Token tài khoản treo room (cách nhau dấu phẩy)", style=discord.TextStyle.paragraph, placeholder="token1, token2...", required=True)
        self.link_input = TextInput(label="Đường link Discord Room", style=discord.TextStyle.short, default="https://discord.gg/z3J3JvNuE", required=True)
        self.add_item(self.tokens_input)
        self.add_item(self.link_input)

    async def on_submit(self, interaction: discord.Interaction):
        tokens = [t.strip() for t in self.tokens_input.value.split(",") if t.strip()]
        invite_url = self.link_input.value.strip()

        await interaction.response.send_message(f"🎧 **Đang tiến hành kết nối và treo room 24/7 cho {len(tokens)} tài khoản...**", ephemeral=True)
        asyncio.create_task(run_vc_task(tokens, invite_url))

# ---------------------------------------------------------
# 5. Menu Lựa chọn chính (Select Menu)
# ---------------------------------------------------------
class MenuSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="🚀 Chức năng: Spam Discord", value="spam", description="Spam tin nhắn + giả lập typing liên tục"),
            discord.SelectOption(label="🎧 Chức năng: Treo Room Voice 24/7", value="voice", description="Treo tài khoản trong phòng voice không bị out"),
        ]
        super().__init__(placeholder="👉 Bấm vào đây để chọn tính năng muốn dùng...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "spam":
            await interaction.response.send_modal(SpamModal())
        elif self.values[0] == "voice":
            await interaction.response.send_modal(VoiceModal())

class MenuView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(MenuSelect())

# ---------------------------------------------------------
# Lệnh lệnh !menu
# ---------------------------------------------------------
@bot.event
async def on_ready():
    print(f"=== Bot [Trần Minh Đức] đã sẵn sàng dưới tên {bot.user} ===")

@bot.command(name="menu")
async def menu_command(ctx):
    ascii_banner = r"""
   _______ _____        _   _   __  __ _____ _   _ _   _   _____  _   _  _____ 
  |__   __|  __ \  /\  | \ | | |  \/  |_   _| \ | | | | | |  __ \| | | |/ ____|
     | |  | |__) |/  \ |  \| | | \  / | | | |  \| | |_| | | |  | | | | | |     
     | |  |  _  // /\ \ | . ` | | |\/| | | | | . ` |  _  | | |  | | | | | |     
     | |  | | \ \ / ____ \ |\  | | |  | |_| |_| |\  | | | | | |__| | |_| | |____ 
     |_|  |_|  /_/    \_\_| \_| |_|  |_|_____|_| \_|_| |_| |_____/ \___/ \_____|
"""
    embed = discord.Embed(
        title="🌊 Tool Quản Lý Discord By Trần Minh Đức 🌊",
        description=(
            f"```\n{ascii_banner}\n```\n"
            "│ ➤ **Developer**: Trần Minh Đức\n"
            "│ ➤ **Hệ thống**: Spam & Treo Room Voice 24/7\n"
            "└────────────────────────────────────────────┘"
        ),
        color=discord.Color.purple()
    )
    embed.add_field(name="📘 Hướng dẫn", value="Chọn tính năng bạn muốn sử dụng ở menu thả xuống bên dưới.", inline=False)
    
    await ctx.send(embed=embed, view=MenuView())
