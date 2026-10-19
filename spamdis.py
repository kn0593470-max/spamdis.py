import os
import aiohttp
import asyncio
import random
import json
import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput

TOKEN_FILE = "user_tokens.json"

# ---------------------------------------------------------
# Quản lý Token Riêng Theo User ID
# ---------------------------------------------------------
def load_user_tokens():
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_user_tokens(data):
    try:
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception:
        pass

def get_tokens_for_user(user_id, raw_input):
    if raw_input.strip().lower() == "my":
        data = load_user_tokens()
        return data.get(str(user_id), [])
    return [t.strip() for t in raw_input.split(",") if t.strip()]

def mask_token(token):
    if len(token) > 15:
        return token[:10] + "..." + token[-5:]
    return token

# ---------------------------------------------------------
# Hàm Kiểm Tra Token Hợp Lệ & Kiểm Tra Join Server
# ---------------------------------------------------------
async def validate_and_filter_tokens(tokens, target_channel_id):
    """
    Kiểm tra danh sách token:
    1. Token sống hay chết (lấy guild_id từ channel)
    2. Token đã join Server chưa
    Trả về: (valid_tokens_for_run, invalid_count, not_joined_tokens)
    """
    valid_tokens = []
    not_joined_tokens = []
    invalid_count = 0
    
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        for token in tokens:
            headers = {
                "Authorization": token.strip(),
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Android; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0"
            }
            try:
                # Lấy thông tin kênh để kiểm tra token có quyền truy cập / đã join server chưa
                async with session.get(f"https://discord.com/api/v10/channels/{target_channel_id}", headers=headers) as resp:
                    if resp.status == 200:
                        valid_tokens.append(token.strip())
                    elif resp.status in (401, 400): # Token sai hoặc hỏng
                        invalid_count += 1
                    elif resp.status in (403, 404): # Token sống nhưng chưa join server hoặc không có quyền truy cập kênh
                        not_joined_tokens.append(token.strip())
                    elif resp.status == 429: # Rate limit -> Tạm thời cho vào danh sách chạy
                        valid_tokens.append(token.strip())
                    else:
                        invalid_count += 1
            except Exception:
                invalid_count += 1

    return valid_tokens, invalid_count, not_joined_tokens

# ---------------------------------------------------------
# Kho Ngôn Mặc Định
# ---------------------------------------------------------
MESSAGES = [
    "sao m rụng ngay khi anh đến r",
    "mồ côi thắp hương cha mẹ trc khi chửi chưa",
    "mồ côi không cha mẹ đổ thừa cay bố m kìa",
    "tao thánh chửi mà :))",  
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
    "con cave này adr 16gb đg kiếm tiền mua ip đk🤣🤣",
    "Vào 1 hôm bỗng con đĩ mẹ nhà m die thì lúc đó cha làm bá chủ sàn mẹ r :))",
    "con đĩ mẹ mày bất lực vì bị tao chửi mà chỉ biết câm lặng:))",
    "mẹ mày bị t đụ đột quỵ ngoài nhà nghỉ kìa đem hòm ra nha",
    "đem hai cái mày với con mẹ m luôn nha",
    "thời gian trôi qua để cảm nhận nỗi đau đi ửa à",
    "nhai t chặt đầu con đĩ má m ra đó",
    "thằng ngu lgbt da đen sủa lẹ ai cko mày câm",
    "thằng sex thú đang cố làm cha cay hả thằng bại não",
    "tao miễn nhiễm mà thằng ngu",
    "Anh Bá Vcl Lỡ Đá Chết Mẹ mày Rồi  😝 👎",
    "Mẹ Mày Bị Cha Đụ Từ Nam Vào Đến Bắc Mà 🤪 👊",
    "Mẹ Mày Banh Háng Cho Khách Đụ Kìa Thằng Óc",
    "Tao Lỡ Cho Mẹ Mày Bú Cu Tao Rồi Sướng Vãi Cặc🧐 🤙",
    "Lêu Lêu Nhìn Cha Đụ Mẹ Mày Ko Làm Được Gì À Đừng Có Cay Cha Nha 😝 👎",
    "bị tao khủng bố quá nát mẹ cái hộp sọ với não luôn rồi à =))",
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
    "mẹ mày bị t địt rách màn trinh mà🤪",
    "🤭🤭Mày bê đê ngũ sắc dell công khai bị tao chọc quá máu cặc mày dồn lên brain choa mày chết hả",
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
async def run_spam_task(tokens, channels, mention_ids, delay, mode):
    headers_list = [{"Authorization": t.strip(), "Content-Type": "application/json"} for t in tokens if t.strip()]
    channel_list = [c.strip() for c in channels if c.strip()]
    if not headers_list or not channel_list:
        return
    mention_text = " ".join([f"<@{uid}>" for uid in mention_ids]) if mention_ids else ""
    
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            if mode == "1":
                while True:
                    for msg in MESSAGES:
                        for idx, headers in enumerate(headers_list):
                            channel_id = channel_list[idx % len(channel_list)]
                            await send_spam_msg(session, headers, channel_id, mention_text, msg, delay)
                        await asyncio.sleep(delay)
            elif mode == "2":
                while True:
                    msg = random.choice(MESSAGES)
                    for idx, headers in enumerate(headers_list):
                        channel_id = channel_list[idx % len(channel_list)]
                        await send_spam_msg(session, headers, channel_id, mention_text, msg, delay)
                    await asyncio.sleep(delay)
            elif mode == "3":
                while True:
                    available_msgs = MESSAGES.copy()
                    random.shuffle(available_msgs)
                    for idx, headers in enumerate(headers_list):
                        if not available_msgs:
                            break
                        msg = available_msgs.pop(0)
                        channel_id = channel_list[idx % len(channel_list)]
                        asyncio.create_task(send_spam_msg(session, headers, channel_id, mention_text, msg, delay))
                    await asyncio.sleep(delay + 1.0)
    except asyncio.CancelledError:
        pass

async def send_spam_msg(session, headers, channel_id, mention_text, msg, delay):
    custom_headers = {
        **headers,
        "User-Agent": "Mozilla/5.0 (Android; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0"
    }
    typing_url = f"https://discord.com/api/v10/channels/{channel_id}/typing"
    send_url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    try:
        async with session.post(typing_url, headers=custom_headers) as resp:
            if resp.status in (403, 503):
                await asyncio.sleep(5)
                return
            elif resp.status == 429:
                data = await resp.json()
                await asyncio.sleep(data.get("retry_after", 1.0))
                
        await asyncio.sleep(delay)
        full_msg = f"{mention_text} {msg}" if mention_text else msg
        
        async with session.post(send_url, json={"content": full_msg}, headers=custom_headers) as resp:
            if resp.status in (403, 503):
                await asyncio.sleep(10)
            elif resp.status == 429:
                try:
                    data = await resp.json()
                    await asyncio.sleep(data.get("retry_after", 2.0))
                except Exception:
                    await asyncio.sleep(5)
    except Exception:
        pass

# ---------------------------------------------------------
# Tiến trình Treo Voice
# ---------------------------------------------------------
async def keep_alive_voice(token, channel_id):
    ws_url = "wss://gateway.discord.gg/?v=10&encoding=json"
    headers = {
        "Authorization": token.strip(), 
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Android; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0"
    }
    
    while True:
        guild_id = None
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout, connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.get(f"https://discord.com/api/v10/channels/{channel_id}", headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        guild_id = data.get("guild_id")
                    elif resp.status in (403, 503):
                        await asyncio.sleep(15)
                        continue
                    elif resp.status == 429:
                        await asyncio.sleep(5)
                        continue
                    else:
                        await asyncio.sleep(5)
                        continue
                
                if not guild_id:
                    await asyncio.sleep(5)
                    continue

                async with session.ws_connect(ws_url, heartbeat=None) as ws:
                    await ws.send_json({
                        "op": 2,
                        "d": {
                            "token": token,
                            "capabilities": 509,
                            "properties": {"os": "Android", "browser": "Discord Android", "device": "Android"}
                        }
                    })
                    await ws.send_json({
                        "op": 4,
                        "d": {"guild_id": guild_id, "channel_id": channel_id, "self_mute": True, "self_deaf": True}
                    })
                    
                    heartbeat_interval = 20.0
                    async def sender(websocket):
                        try:
                            while not websocket.closed:
                                await asyncio.sleep(heartbeat_interval)
                                await websocket.send_json({"op": 1, "d": None})
                        except Exception:
                            pass

                    send_task = asyncio.create_task(sender(ws))
                    try:
                        async for msg in ws:
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                data = msg.json()
                                if data.get("op") == 10:
                                    heartbeat_interval = data["d"].get("heartbeat_interval", 20000) / 1000.0
                            elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                                break
                    finally:
                        send_task.cancel()
        except asyncio.CancelledError:
            break 
        except Exception:
            pass
        await asyncio.sleep(5)

# ---------------------------------------------------------
# Modal Forms
# ---------------------------------------------------------
class SpamModal(Modal, title="Cấu hình Tool Discord - Spam"):
    tokens_input = TextInput(label="Token (Dán trực tiếp hoặc gõ 'my')", style=discord.TextStyle.paragraph, placeholder="token1, token2... hoặc gõ 'my'", required=True)
    channels_input = TextInput(label="ID Kênh (Ngăn cách bằng dấu phẩy)", style=discord.TextStyle.short, placeholder="id_kenh_1...", required=True)
    tags_input = TextInput(label="ID Tag (Để trống nếu không tag)", style=discord.TextStyle.short, required=False)
    mode_input = TextInput(label="Chế độ (1: Tuần tự | 2: Ngẫu nhiên | 3: Không trùng)", style=discord.TextStyle.short, default="3", required=True)
    delay_input = TextInput(label="Delay (giây)", style=discord.TextStyle.short, default="1.0", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True) # Tránh bị timeout khi lọc token
        
        raw_tokens = get_tokens_for_user(interaction.user.id, self.tokens_input.value)
        if not raw_tokens:
            await interaction.followup.send("❌ **Kho token trống! Hãy gõ `!settoken` trước.**", ephemeral=True)
            return

        channels = [c.strip() for c in self.channels_input.value.split(",") if c.strip()]
        if not channels:
            await interaction.followup.send("❌ **Vui lòng nhập ID Kênh hợp lệ!**", ephemeral=True)
            return

        target_channel = channels[0]
        valid_tokens, invalid_count, not_joined_tokens = await validate_and_filter_tokens(raw_tokens, target_channel)

        msg_report = []
        if invalid_count > 0:
            msg_report.append(f"⚠️ **Đã tự động loại bỏ {invalid_count} Token sai/hỏng!**")
        
        if not_joined_tokens:
            masked_list = "\n".join([f"• `{mask_token(t)}`" for t in not_joined_tokens])
            msg_report.append(f"🔴 **Phát hiện {len(not_joined_tokens)} Token CHƯA JOIN SERVER! Hãy cho các token này join server trước:**\n{masked_list}")

        if not valid_tokens:
            msg_report.append("❌ **Không có token nào hợp lệ và đã join server để chạy!**")
            await interaction.followup.send("\n\n".join(msg_report), ephemeral=True)
            return

        mention_ids = [m.strip() for m in self.tags_input.value.split(",") if m.strip()]
        mode = self.mode_input.value.strip() if self.mode_input.value.strip() in ["1", "2", "3"] else "3"
        try:
            delay = float(self.delay_input.value.strip())
        except ValueError:
            delay = 1.0

        msg_report.append(f"⚡ **Khởi chạy Spam (Chế độ {mode}) thành công cho {len(valid_tokens)} Token hợp lệ!**")
        await interaction.followup.send("\n\n".join(msg_report), ephemeral=True)

        task = asyncio.create_task(run_spam_task(valid_tokens, channels, mention_ids, delay, mode))
        active_spam_tasks.append(task)

class VoiceModal(Modal, title="Cấu hình Treo Room Voice 24/7"):
    tokens_input = TextInput(label="Token tài khoản (Dán trực tiếp hoặc gõ 'my')", style=discord.TextStyle.paragraph, placeholder="token1, token2... hoặc gõ 'my'", required=True)
    channel_id_input = TextInput(label="ID Phòng Voice", style=discord.TextStyle.short, placeholder="Nhập ID Phòng...", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        raw_tokens = get_tokens_for_user(interaction.user.id, self.tokens_input.value)
        if not raw_tokens:
            await interaction.followup.send("❌ **Kho token trống! Hãy gõ `!settoken` trước.**", ephemeral=True)
            return

        channel_id = self.channel_id_input.value.strip()
        valid_tokens, invalid_count, not_joined_tokens = await validate_and_filter_tokens(raw_tokens, channel_id)

        msg_report = []
        if invalid_count > 0:
            msg_report.append(f"⚠️ **Đã tự động loại bỏ {invalid_count} Token sai/hỏng!**")
        
        if not_joined_tokens:
            masked_list = "\n".join([f"• `{mask_token(t)}`" for t in not_joined_tokens])
            msg_report.append(f"🔴 **Phát hiện {len(not_joined_tokens)} Token CHƯA JOIN SERVER! Vui lòng cho join server trước:**\n{masked_list}")

        if not valid_tokens:
            msg_report.append("❌ **Không có token nào hợp lệ và đã join server để treo voice!**")
            await interaction.followup.send("\n\n".join(msg_report), ephemeral=True)
            return

        msg_report.append(f"🎧 **Đã bật Treo Room Voice cho {len(valid_tokens)} Token hợp lệ!**")
        await interaction.followup.send("\n\n".join(msg_report), ephemeral=True)

        for token in valid_tokens:
            task = asyncio.create_task(keep_alive_voice(token, channel_id))
            active_vc_tasks.append(task)

class SetTokenModal(Modal, title="Lưu Kho Token Cá Nhân"):
    tokens_input = TextInput(label="Nhập danh sách Token (Ngăn cách bằng dấu phẩy)", style=discord.TextStyle.paragraph, placeholder="token1, token2, token3...", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        tokens = [t.strip() for t in self.tokens_input.value.split(",") if t.strip()]
        if not tokens:
            await interaction.response.send_message("⚠️ **Không tìm thấy token hợp lệ!**", ephemeral=True)
            return
        data = load_user_tokens()
        data[user_id] = tokens
        save_user_tokens(data)
        await interaction.response.send_message(f"✅ **Đã lưu {len(tokens)} token vào kho cá nhân của bạn!**", ephemeral=True)

# ---------------------------------------------------------
# Interactive Menu View
# ---------------------------------------------------------
class MenuView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🚀 Khởi Chạy Spam", style=discord.ButtonStyle.green, custom_id="btn_spam_persistent")
    async def spam_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(SpamModal())

    @discord.ui.button(label="🎧 Treo Room Voice", style=discord.ButtonStyle.blurple, custom_id="btn_voice_persistent")
    async def voice_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(VoiceModal())

    @discord.ui.button(label="🔑 Lưu Token Cá Nhân", style=discord.ButtonStyle.gray, custom_id="btn_settoken_persistent")
    async def settoken_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(SetTokenModal())

    @discord.ui.button(label="🛑 Dừng Spam", style=discord.ButtonStyle.red, custom_id="btn_stopsp_persistent")
    async def stopsp_button(self, interaction: discord.Interaction, button: Button):
        global active_spam_tasks
        if not active_spam_tasks:
            await interaction.response.send_message("⚠️ Không có tiến trình spam nào!", ephemeral=True)
            return
        count = len(active_spam_tasks)
        for task in active_spam_tasks:
            task.cancel()
        active_spam_tasks.clear()
        await interaction.response.send_message(f"🛑 Đã dừng {count} tiến trình Spam!", ephemeral=True)

    @discord.ui.button(label="❌ Dừng Treo Voice", style=discord.ButtonStyle.red, custom_id="btn_stoprom_persistent")
    async def stoprom_button(self, interaction: discord.Interaction, button: Button):
        global active_vc_tasks
        if not active_vc_tasks:
            await interaction.response.send_message("⚠️ Không có tài khoản nào treo room!", ephemeral=True)
            return
        count = len(active_vc_tasks)
        for task in active_vc_tasks:
            task.cancel()
        active_vc_tasks.clear()
        await interaction.response.send_message(f"🛑 Đã dừng treo voice cho {count} tài khoản!", ephemeral=True)

# ---------------------------------------------------------
# Lệnh Chat Direct (Đã cập nhật Auto-Check)
# ---------------------------------------------------------
@bot.command(name="settoken")
async def set_token_cmd(ctx, *, tokens_str: str = None):
    if not tokens_str:
        await ctx.send(f"⚠️ **Cú pháp:** `!settoken token1, token2...`")
        return
    tokens = [t.strip() for t in tokens_str.split(",") if t.strip()]
    data = load_user_tokens()
    data[str(ctx.author.id)] = tokens
    save_user_tokens(data)
    await ctx.send(f"✅ **Đã lưu thành công {len(tokens)} token cho {ctx.author.mention}!**")

@bot.command(name="mytoken")
async def my_token_cmd(ctx):
    tokens = load_user_tokens().get(str(ctx.author.id), [])
    if not tokens:
        await ctx.send("⚠️ **Kho token của bạn đang trống! Hãy dùng `!settoken` hoặc bấm nút Lưu Token trên Menu.**")
        return
    masked = [mask_token(t) for t in tokens]
    await ctx.send(f"📂 **Kho token cá nhân ({len(tokens)} token):**\n```yaml\n" + "\n".join(masked) + "\n```")

@bot.command(name="spam")
async def spam_cmd(ctx, tokens_input: str, channels_input: str, mode: str = "3", delay: float = 1.0, *, tags_input: str = ""):
    raw_tokens = get_tokens_for_user(ctx.author.id, tokens_input)
    if not raw_tokens:
        await ctx.send("❌ **Không tìm thấy token! Hãy gõ `!settoken` trước.**")
        return
    channels = [c.strip() for c in channels_input.split(",") if c.strip()]
    if not channels:
        await ctx.send("❌ **Vui lòng nhập ID Kênh!**")
        return

    valid_tokens, invalid_count, not_joined_tokens = await validate_and_filter_tokens(raw_tokens, channels[0])

    if invalid_count > 0:
        await ctx.send(f"⚠️ **Đã tự động loại bỏ {invalid_count} Token sai/hỏng!**")

    if not_joined_tokens:
        masked_list = "\n".join([f"• `{mask_token(t)}`" for t in not_joined_tokens])
        await ctx.send(f"🔴 **Phát hiện {len(not_joined_tokens)} Token CHƯA JOIN SERVER! Hãy cho join server trước:**\n{masked_list}")

    if not valid_tokens:
        await ctx.send("❌ **Không có token nào hợp lệ và đã join server để chạy!**")
        return

    mention_ids = [m.strip() for m in tags_input.split(",") if m.strip()]
    await ctx.send(f"⚡ **Khởi chạy Spam (Chế độ {mode}) cho {len(valid_tokens)} Token hợp lệ!**")
    task = asyncio.create_task(run_spam_task(valid_tokens, channels, mention_ids, delay, mode))
    active_spam_tasks.append(task)

@bot.command(name="voice")
async def voice_cmd(ctx, tokens_input: str, channel_id: str):
    raw_tokens = get_tokens_for_user(ctx.author.id, tokens_input)
    if not raw_tokens:
        await ctx.send("❌ **Không tìm thấy token! Hãy gõ `!settoken` trước.**")
        return

    valid_tokens, invalid_count, not_joined_tokens = await validate_and_filter_tokens(raw_tokens, channel_id)

    if invalid_count > 0:
        await ctx.send(f"⚠️ **Đã tự động loại bỏ {invalid_count} Token sai/hỏng!**")

    if not_joined_tokens:
        masked_list = "\n".join([f"• `{mask_token(t)}`" for t in not_joined_tokens])
        await ctx.send(f"🔴 **Phát hiện {len(not_joined_tokens)} Token CHƯA JOIN SERVER! Vui lòng cho join server trước:**\n{masked_list}")

    if not valid_tokens:
        await ctx.send("❌ **Không có token nào hợp lệ và đã join server để treo voice!**")
        return

    await ctx.send(f"🎧 **Đã bật Treo Room Voice cho {len(valid_tokens)} Token hợp lệ!**")
    for token in valid_tokens:
        task = asyncio.create_task(keep_alive_voice(token, channel_id))
        active_vc_tasks.append(task)

@bot.command(name="loadtxt")
async def load_txt_cmd(ctx):
    if not ctx.message.attachments or not ctx.message.attachments[0].filename.endswith(".txt"):
        await ctx.send("⚠️ **Vui lòng gửi kèm file `.txt` (mỗi dòng 1 câu)!**")
        return
    try:
        content = (await ctx.message.attachments[0].read()).decode("utf-8", errors="ignore")
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        if lines:
            global MESSAGES
            MESSAGES = lines
            await ctx.send(f"✅ **Đã nạp {len(MESSAGES)} câu ngôn mới từ file!**")
    except Exception as e:
        await ctx.send(f"❌ **Lỗi:** `{e}`")

@bot.command(name="stopsp")
async def stop_spam_cmd(ctx):
    global active_spam_tasks
    if not active_spam_tasks:
        await ctx.send("⚠️ Không có tiến trình spam nào!")
        return
    count = len(active_spam_tasks)
    for task in active_spam_tasks:
        task.cancel()
    active_spam_tasks.clear()
    await ctx.send(f"🛑 **Đã dừng {count} tiến trình Spam!**")

@bot.command(name="stoprom")
async def stop_room_cmd(ctx):
    global active_vc_tasks
    if not active_vc_tasks:
        await ctx.send("⚠️ Không có tài khoản nào treo room!")
        return
    count = len(active_vc_tasks)
    for task in active_vc_tasks:
        task.cancel()
    active_vc_tasks.clear()
    await ctx.send(f"🛑 **Đã ngắt treo voice cho {count} tài khoản!**")

@bot.command(name="menu")
async def menu_cmd(ctx):
    embed = discord.Embed(
        title="⚡ TOOL DISCORD - HỆ THỐNG CHIẾN WAR ⚡",
        description="```yaml\n          Tự Động Lọc Token Sai & Kiểm Tra Join Server     \n```",
        color=discord.Color.red()
    )
    embed.add_field(
        name="📘 Bảng Thao Tác",
        value=(
            "• **🚀 Khởi Chạy Spam**: Tự động lọc token sai & chưa join server.\n"
            "• **🎧 Treo Room Voice**: Chỉ treo những token hợp lệ.\n"
            "• **🔑 Lưu Token Cá Nhân**: Lưu trữ kho token riêng.\n"
            "• **🛑 Dừng Spam / ❌ Dừng Voice**: Bấm dừng trực tiếp."
        ),
        inline=False
    )
    await ctx.send(embed=embed, view=MenuView())

@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(
        title="📖 HƯỚNG DẪN SỬ DỤNG TOOL DISCORD",
        description="Hệ thống tự động lọc token lỗi & chưa join server.",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="✨ Tính năng lọc thông minh",
        value=(
            "• Khi kích hoạt Spam hoặc Voice, bot sẽ quét toàn bộ token.\n"
            "• Nếu có **Token Sai/Lỗi**: Bot sẽ báo số lượng và tự động loại bỏ.\n"
            "• Nếu có **Token Chưa Join Server**: Bot sẽ liệt kê danh sách token đó và bắt buộc bạn phải dùng tài khoản đó tham gia server trước."
        ),
        inline=False
    )
    await ctx.send(embed=embed)

async def bot_keep_alive():
    while True:
        await asyncio.sleep(30)
        if bot.is_ready():
            try:
                await bot.change_presence(activity=discord.Game(name="!menu | Auto-Check Token Online"))
            except Exception:
                pass

@bot.event
async def on_ready():
    bot.add_view(MenuView())
    print(f"=== Tool Discord đã sẵn sàng dưới tên {bot.user} ===")
    bot.loop.create_task(bot_keep_alive())
