import json
import logging
import threading
import rg_javascript

from rg_javascript import require, On

mineflayer_pathfinder = require('mineflayer-pathfinder')
mineflayer = require('mineflayer', '4.5.1')
rg_match_info = require('rg-match-info')
Vec3 = require('vec3').Vec3
nbt = require("prismarine-nbt")
rg_bot = require('rg-bot', '1.4.0')

logging.basicConfig(level=logging.NOTSET)

# We keep track of deaths to make sure that this bot stops when it dies
deaths = 0

am_hunting = False

# If there are no animals around, have it attack you by adding
# "player" to this list.
animals_to_hunt = ["chicken", "pig", "cow", "sheep", "rabbit"]


def configure_bot(bot):

  logging.info('configure_bot called for player bot')

  bot.setDebug(True)
  bot.allowParkour(False)
  bot.allowDigWhilePathing(True)

  # This function finds animals, attacks them until they are dead, and
  # then picks up their items.
  def hunt_animal():
    nearby_animals = bot.findEntities({
      'entityNames': animals_to_hunt,
      'maxDistance': 100
    })
    logging.info(
      f"Found {nearby_animals.length} nearby animals to hunt: {nearby_animals}"
    )

    if nearby_animals.length == 0:
      return False
    animal_to_attack = nearby_animals[0].result
    animal_name = animal_to_attack.name
    bot.chat(f"Hunting a {animal_name}")

    # Edge case: If we fail to attack many times, or the bot failed to
    # attack at all, skip this animal
    attack_count = 0
    did_attack = True
    while did_attack and animal_to_attack.isValid and attack_count < 50:
      logging.info(f"Attacking the {animal_name}")
      attack_count = attack_count + 1
      did_attack = bot.attackEntity(animal_to_attack)

    bot.chat(
      f"Finished attacking the {animal_name}, moving on the next victim")
    # Exit on the first loop to simulate safely accessing array element index 0
    return True

  # This function allows us to repeatedly call the huntAnimals function
  # until the bot dies
  def repeat_hunt_animals():
    global am_hunting
    if not am_hunting:
      am_hunting = True

      def long_running_task(**kwargs):
        global am_hunting
        try:
          # Edge case: the bot will wander further every time it can't find an animal
          wander_min_distance = 1

          global deaths
          # While the bot has not died again (i.e. the count has not increased),
          # try to find an animal again.
          previous_deaths = deaths

          while previous_deaths == deaths:
            logging.info('Starting a hunt animals loop')
            did_hunt_and_kill = hunt_animal()
            if did_hunt_and_kill:
              wander_min_distance = 1
              items_on_ground = bot.findAndCollectItemsOnGround()
            else:
              bot.chat(
                f"Could not find animals nearby... going to wander {wander_min_distance} to {wander_min_distance*2} and try again"
              )
              bot.wander(wander_min_distance, wander_min_distance * 2)
              wander_min_distance = wander_min_distance + 1
        except Exception as ere:
          logging.exception('Something bad happened to my code: %r', ere)
        finally:
          am_hunting = False

      thread = threading.Thread(target=long_running_task, kwargs={})
      thread.start()

  @On(bot, 'spawn')
  def bot_on_spawn(this):
    bot.chat('I have arrived... ready to hunt some animals!')

  # Record deaths by incrementing our counter every time we die
  @On(bot, 'death')
  def bot_on_death(this):
    global deaths
    deaths = deaths + 1

  # Only start hunting once we ask the bot to start
  @On(bot, 'chat')
  def bot_on_chat(this, username, message, *args):
    # logging.info(f"Received chat from {username} - {message}")
    if username == bot.username():
      return
    if message.strip() == "hunt":
      repeat_hunt_animals()

  @On(bot, 'kicked')
  def bot_on_kicked(this, reason):
    bot.chat('I was kicked for a reason: %r', reason)

  @On(bot, 'error')
  def bot_on_error(this, error):
    bot.chat('I encountered an error: %r', error)
