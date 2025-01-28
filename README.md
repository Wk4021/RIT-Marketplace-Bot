# 🐯 RIT Marketplace Bot

*A Discord bot powering safe peer-to-peer transactions for RIT students*

[![Discord](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/your-invite-link)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![GitHub Release](https://img.shields.io/github/v/release/Wk4021/RIT-Marketplace-Bot?style=for-the-badge&color=blue)](https://github.com/Wk4021/RIT-Marketplace-Bot/releases)
[![RIT Community](https://img.shields.io/badge/RIT-Community-orange?style=for-the-badge&logo=bookstack)](https://www.rit.edu)

## 🚀 Features

### 🔥 Current Features
| Category               | Features                                                                                     |
|------------------------|---------------------------------------------------------------------------------------------|
| **📝 Post Management**  | - ✅ TOS agreement system<br>- ⏳ Auto-expiration (7d/30d)<br>- 🗑️ Self-deletion              |
| **⭐ Reputation**       | - ★★★★★ Rating system<br>- 📊 Public profiles<br>- 🔒 Low-reputation locking                |
| **🛡️ Moderation**      | - 🚩 User reporting<br>- 🔨 Force-close commands<br>- 📜 Action logging                     |
| **💎 Premium**         | - 🕑 Extended duration<br>- 🔄 Priority renewal<br>- 📈 Advanced analytics (Coming Soon)     |

### 📋 Command Reference
| Command                | Description                          | Permission          |
|------------------------|--------------------------------------|---------------------|
| `📢 /report [reason]`  | Flag problematic posts               | 👥 All Users        |
| `🗑️ /remove`           | Delete your post                     | ✍️ Post Author      |
| `🔒 /force_close`      | Moderator close post                 | 🛡️ Moderators       |
| `⭐ /rep [user]`        | Check reputation                     | 👥 All Users        |
| `💬 /rate [user]`      | Rate transaction partner             | 🤝 Participants     |

## 🚧 Coming Soon Features
```diff
+ 🆕 Post Renewal System          
+ 🔔 Expiry Reminders             
+ 📈 Rating Analytics             
+ 🏷️ Category Templates           
```

## 🛠️ Installation Guide

### 📋 Prerequisites
- Python 3.10+
- [Community-Enabled Discord Server](https://support.discord.com/hc/en-us/articles/360047132851-Enabling-Your-Community-Server)
- #️⃣ Forum Channel Setup

### ⚙️ Setup
```bash
# 1. Clone repository
git clone https://github.com/Wk4021/RIT-Marketplace-Bot.git
cd RIT-Marketplace-Bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
echo "TOKEN=your_bot_token_here
GUILD_ID=   #your_server_id
PREMIUM_ROLE_ID =   # Your premium role ID
LOG_CHANNEL_ID =   # Default log channel ID
TOS_CHANNEL_ID =   # Your TOS channel ID" > .env

# 4. Launch bot
python bot.py
```

## 🤝 Contributing

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](https://makeapullrequest.com)
[![Good First Issues](https://img.shields.io/github/issues/Wk4021/RIT-Marketplace-Bot/good%20first%20issue?style=for-the-badge&color=purple)](https://github.com/Wk4021/RIT-Marketplace-Bot/issues)

### 🛣️ Contribution Workflow
1. **🔍 Find an Issue** - Check our [issue board](https://github.com/Wk4021/RIT-Marketplace-Bot/issues)
2. **💻 Development**  
   ```bash
   git checkout -b feature/your-feature
   # Make magic happen ✨
   git commit -m "feat: add amazing feature"
   git push origin feature/your-feature
   ```
3. **📮 Submit PR** 

### 🧑💻 Coding Standards
- **📚 Documentation:** All new features require docstrings
- **🧪 Testing:** 80%+ coverage for new code
- **🎨 Style:** PEP-8 compliant with type hints
- **🔗 Discord:** Follow [best practices](https://discordpy.readthedocs.io/en/stable/)

## 📜 License
MIT License © 2023 [Your Name]  
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)

---

⚠️ **Disclaimer**  
*This project is not officially affiliated with Rochester Institute of Technology. Always verify transactions and exercise caution when trading.*
