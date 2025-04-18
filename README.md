# Discord Server Setup Bot

This bot automatically creates a complete server structure for a digital agency's virtual office in Discord.

## Features

- Automatically creates categories and channels
- Sets up department-specific channels
- Creates voice channels for meetings
- Configures roles for different team members
- Includes both setup and cleanup commands

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create a Discord Bot**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to the "Bot" section
   - Create a bot and copy the token
   - Enable the following Privileged Gateway Intents:
     - Message Content Intent
     - Server Members Intent

3. **Configure the Bot**
   - Copy your bot token
   - Edit the `.env` file and replace `your_bot_token_here` with your actual bot token

4. **Invite the Bot**
   - Go to OAuth2 > URL Generator in the Developer Portal
   - Select the following scopes:
     - `bot`
     - `applications.commands`
   - Select the following permissions:
     - Administrator (required for server setup)
   - Copy and use the generated URL to invite the bot to your server

5. **Run the Bot**
   ```bash
   python bot.py
   ```

## Usage

Once the bot is running and invited to your server:

- `!setup` - Creates the complete server structure
- `!clean` - Removes all channels and categories (use with caution!)

Note: Only users with Administrator permissions can use these commands.

## Server Structure

The bot creates the following structure:

### Categories and Channels
- 📢 INFORMATION
  - welcome
  - announcements
  - rules
  - company-info
- 💼 WORK
  - general
  - projects
  - deadlines
  - resources
  - client-updates
- 👥 DEPARTMENTS
  - design-team
  - development-team
  - marketing-team
  - sales-team
- 📋 PROJECT COORDINATION
  - project-planning
  - task-assignments
  - quality-assurance
- 🎤 MEETING ROOMS (Voice Channels)
  - Team Standup
  - Client Meetings
  - Brainstorming
  - General Discussion

### Roles
- Admin
- Manager
- Developer
- Designer
- Marketing
- Sales
- Client 