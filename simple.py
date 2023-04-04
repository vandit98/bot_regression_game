from rg_javascript import require, On

# Import any libraries you need, even your JS libs!
mineflayer_pathfinder = require('mineflayer-pathfinder')
mineflayer = require('mineflayer', '4.5.1')


def configure_bot(bot):

  @On(bot, 'chat')
  def bot_on_chat(this, username, message, *args):
    if username == bot.username():
      return
    bot.chat('This is what I heard: ' + message)
