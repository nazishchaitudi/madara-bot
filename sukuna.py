# 𝑹𝑰𝑺𝑯𝑰~♤_bot_multi.py
import asyncio
import json
import os
import random
import time
import telegram.error
from datetime import datetime, timedelta, timezone
from telegram import Update, InputSticker, Sticker
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging
import yt_dlp
from gtts import gTTS
import requests
import io

# ---------------------------
# CONFIG
# ---------------------------
TOKENS = [
'8908448387:AAGWpEH3Mh8Pa1mPQ1aMPJhvbJoVEgotkDw',
'8596316387:AAGtF040jegDGm1u1zBE65wKPxqKvRk0YYw',
'8929975338:AAGPySari1jJYSIH4lTz_4j0cqIONNDptRU',
'8684565840:AAHH7hl0IvuAPp4mUx1JVQgWGTpb7s_otSA',
'8885185791:AAHgt0rPytjXIR7X4a1uyVa347evIMETzg0',
'8859137340:AAEmT67IJOJ07GrdEREeX6_44P11DDstT6A',
'8822200987:AAF33GRJUiOoEYqg6YsLKoOGdAjN5E-tor0',
'8715775338:AAHxxBoU9qa0UEymf4yoT1TndDUZRdR5IEU',
'8869820271:AAEpIojWjV-FNFOC0-bXtD4nhqndQoe-4FU',
'8849515274:AAF6LYyMPGIpH6vvzXpuRRw32Eg6f1QDAU8',
]

CHAT_ID = 6467928792
OWNER_ID = 6467928792
SUDO_FILE = "8542011607"
STICKER_FILE = "stickers.json"
VOICE_CLONES_FILE = "voice_clones.json"
tempest_API_KEY = "sk_e326b337242b09b451e8f18041fd0a7149cc895648e36538"  # ✅ YOUR API KEY ADDED

# ---------------------------
# tempest VOICE CHARACTERS
# ---------------------------
VOICE_CHARACTERS = {
    1: {
        "name": "Urokodaki",
        "voice_id": "VR6AewLTigWG4xSOukaG",  # Deep Indian voice
        "description": "Deep Indian voice - Urokodaki style",
        "style": "deep_masculine"
    },
    2: {
        "name": "Kanae", 
        "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Cute sweet voice
        "description": "Cute sweet voice - Kanae style",
        "style": "soft_feminine"
    },
    3: {
        "name": "Uppermoon",
        "voice_id": "AZnzlk1XvdvUeBnXmlld",  # Creepy dark voice
        "description": "Creepy dark deep voice - Uppermoon style", 
        "style": "dark_creepy"
    },
    4: {
        "name": "Tanjiro",
        "voice_id": "VR6AewLTigWG4xSOukaG",
        "description": "Heroic determined voice",
        "style": "heroic"
    },
    5: {
        "name": "Nezuko",
        "voice_id": "EXAVITQu4vr4xnSDxMaL", 
        "description": "Cute mute sounds",
        "style": "cute_mute"
    },
    6: {
        "name": "Zenitsu",
        "voice_id": "AZnzlk1XvdvUeBnXmlld",
        "description": "Scared whiny voice",
        "style": "scared_whiny"
    },
    7: {
        "name": "Inosuke",
        "voice_id": "VR6AewLTigWG4xSOukaG",
        "description": "Wild aggressive voice",
        "style": "wild_aggressive"
    },
    8: {
        "name": "Muzan",
        "voice_id": "AZnzlk1XvdvUeBnXmlld",
        "description": "Evil mastermind voice",
        "style": "evil_calm"
    },
    9: {
        "name": "Shinobu",
        "voice_id": "EXAVITQu4vr4xnSDxMaL",
        "description": "Gentle but deadly voice",
        "style": "gentle_deadly"
    },
    10: {
        "name": "Giyu",
        "voice_id": "VR6AewLTigWG4xSOukaG",
        "description": "Silent serious voice",
        "style": "silent_serious"
    }
}

# ---------------------------
# TEXTS
# ---------------------------
RAID_TEXTS = [
 "×~🌷Teri ma ka अंतिम संस्कार हो गया!!~🙌🏿🤣👏🏿👏🏿🔫🔥🁮nn����~",
"~×🌼क्या  रे 𝐙ᴏᴍᴀᴛᴏ 𝐁ᴏʏ  𝐒ᴘᴀᴍᴍᴇʀ बनेगा 𝐓ᴍᴋᴄ मारू    ִֶָ𓂃 ࣪˖ ִֶָ🐇་༘࿐🌼×𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫~",
"~×🌻𝐍ʏ 𝐍ʏ 𝐌ᴇ 𝐊ᴜᴄʜ 𝐍ʏ 𝐒ᴏɴᴜɢᴀ 𝐓ᴇʀʏ 𝐌ᴀᴀ 𝐑ᴀɴᴅʏ 𝐁ᴀᴀᴛ 𝐊ʜᴀᴛᴀᴍ/-😆😈😜 🤘🏻𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🌻×~",
"~×🌺Teri बुआ ki चूत चोद चोद  के lock 🔐 करदूंगा!! 🤙🏿😍💦🌺×~",
"~×🌹TMKC🌹𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫×~",
"~×🏵️TMR🏵𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫×~️",
"~×🪷TMKB🪷𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫×~",
"~×💮🅺🅰🅱🅷🅸 🅴🅂🅴 🅲🅷🆄🅳🅰🅸 🄺🄷🄰🄸 🅷🅰🅸  𝙂𝙐𝙇𝘼𝙈 🌀🌀 🌀🌀🌀 🌀🌀🌀🌀 🌀🌀🌀🌀🌀 🌀🌀🌀💮𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫×~",
"~×🌸RANDII K BACHEE TALWEEEE CHAT 𝑹𝑰𝑺𝑯𝑰 BAAP K 𝑹𝑰𝑺𝑯𝑰 GOD EY RNDYKE🌸𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫×~",
"~×♡TUU SALE GAREEB🌷×~",
"~×🌼TERI MAA RANDY🌼×~",
"~×🌻जब मैं तेरी माँ को जम कर चोदूंगा तो तेरी माँ रहम की भीख मांगेगी Samjha🌻𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫×~",
"~×🌺TATTI KGA RANIDIKE TU🌺×~",
"~×🌹𝑹𝑰𝑺𝑯𝑰 DADDY NAAM LEE CHOR DUNGA🌹×𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫~",
"~×🏵️CHAMAR K LADKE CHUP 🏵️×~𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫",
"~×🪷SPERM COLLECTOR HAI TUU🪷×~𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫",
"~×💮CHUTI LULLI K KIDEE💮×~",
"~×🌸𝑹𝑰𝑺𝑯𝑰 BAAP NAAM LER FAST🌸×~",
"~×🌷SWIPE KESE LERA 𝑹𝑰𝑺𝑯𝑰 PAPA KO🌷×𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫~",
"~×🌼BHAGNA MNA HAI BACHE🌼×~",
"~×🌻BHAG MAT ABHI 𝑹𝑰𝑺𝑯𝑰 PAPA KII ENTRY HUI🌻×~",
"~×🌺𝑹𝑰𝑺𝑯𝑰 KII ENTRY HATER KII MAA CHODTE HUE🌺×~",
"~×🌹𝑹𝑰𝑺𝑯𝑰 𝑹𝑰𝑺𝑯𝑰 KESE KER RHA GULAMI KER 𝑹𝑰𝑺𝑯𝑰 DADDY KI🌹×~",
"~×🏵️JUST SAY 𝑹𝑰𝑺𝑯𝑰 PAPAᵢ ₗₒᵥₑ ᵧₒᵤ🐍🍀❤️‍🔥🅺🅰🅱🅷🅸 🅴🅂🅴 🅲🅷🆄🅳🅰🅸 🄺🄷🄰🄸 🅷🅰🅸  𝙂𝙐𝙇𝘼𝙈🏵×~️",
"~🪷 🧬 🫧 ᴛᴍᴋᴄ ᴍᴇʜ 🇱 🇦 🇳 🇩 🅳︎🅰︎🅻︎🅺︎🅴︎ 𝙛𝙖𝙖𝙙 ᴅᴜɴɢᴀ🪷~",
"~×💮HAN TERI MA RANDYTERI  𝐌𝐀 𝐊𝐈 𝐂𝐇𝐔𝐓 𝐌 𝐇𝐀𝐓𝐇𝐈 𝐇𝐀𝐌𝐋𝐀 💮×~",
"~×🌸𝐍ʏ 𝐍ʏ 𝐌ᴇ 𝐊ᴜᴄʜ 𝐍ʏ 𝐒ᴏɴᴜɢᴀ 𝐓ᴇʀʏ 𝐌ᴀᴀ 𝐑ᴀɴᴅʏ 𝐁ᴀᴀᴛ 𝐊ʜᴀᴛᴀᴍ/-😆😈😜 🤘🏻🌸×~",
"~×क्या  रे 𝐙ᴏᴍᴀᴛᴏ 𝐁ᴏʏ  𝐒ᴘᴀᴍᴍᴇʀ बनेगा 𝐓ᴍᴋᴄ मारू    ִֶָ𓂃 ࣪˖ ִֶָ🐇་༘࿐🌷×~",
"~×🌼क्या  रे 𝐙ᴏᴍᴀᴛᴏ 𝐁ᴏʏ  𝐒ᴘᴀᴍᴍᴇʀ बनेगा 𝐓ᴍᴋᴄ मारू    ִֶָ𓂃 ࣪˖ ִֶָ🐇་༘࿐🌼×~",
"~×🌻𝐍ʏ 𝐍ʏ 𝐌ᴇ 𝐊ᴜᴄʜ 𝐍ʏ 𝐒ᴏɴᴜɢᴀ 𝐓ᴇʀʏ 𝐌ᴀᴀ 𝐑ᴀɴᴅʏ 𝐁ᴀᴀᴛ 𝐊ʜᴀᴛᴀᴍ/-😆😈😜 🤘🏻 🌻×~",
"~×🌺क्या  रे 𝐙ᴏᴍᴀᴛᴏ 𝐁ᴏʏ  𝐒ᴘᴀᴍᴍᴇʀ बनेगा 𝐓ᴍᴋᴄ मारू    ִֶָ𓂃 ࣪˖ ִֶָ🐇་༘࿐ 🌺×~",
"~×🌹क्या  रे 𝐙ᴏᴍᴀᴛᴏ 𝐁ᴏʏ  𝐒ᴘᴀᴍᴍᴇʀ बनेगा 𝐓ᴍᴋᴄ मारू    ִֶָ𓂃 ࣪˖ ִֶָ🐇་༘࿐🌹×~",
"~×🏵️BIHARI HAI TUU TATTE CHUP🏵×~️",
"~×🪷MULLE CHUP HOJA VERNA TERI MAA CHUD JAYEGI🪷×~",
"~×💮𝐍ʏ 𝐍ʏ 𝐌ᴇ 𝐊ᴜᴄʜ 𝐍ʏ 𝐒ᴏɴᴜɢᴀ 𝐓ᴇʀʏ 𝐌ᴀᴀ 𝐑ᴀɴᴅʏ 𝐁ᴀᴀᴛ 𝐊ʜᴀᴛᴀᴍ/-😆😈😜 🤘🏻 💮×~",
"~×🌸GULAM HAI TUU KIDEE🌸×~",
"~×🌷Teri ma ka अंतिम संस्कार हो गया!!~🙌🏿🤣👏🏿👏🏿🔫🔥🌷×~",
"~×🌼EWW 𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫 🌼×~",
"~×🌻CHOTE TATTE CHUP RANDIKE 𝑹𝑰𝑺𝑯𝑰 BAAP HAI TERA 𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🌻×~",
"~×🌺जब मैं तेरी माँ को जम कर चोदूंगा तो तेरी माँ रहम की भीख मांगेगी Samjha 𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🌺×~",
"~×🌹𝑹𝑰𝑺𝑯𝑰 PAPA KI ENTRY𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫 🌹×~"
]

exonc_TEXTS = [
    "×🌼×","×🌻×","×🪻×","×🏵️×","×💮×","×🌸×","×🪷×","×🌷×",
    "×🌺×","×🥀×","×🌹×","×💐×","×💋×","×❤️‍🔥×","×❤️‍🩹×","×❣️×",
    "×♥️×","×💟×","×💌×","×💕×","×💞×","×💓×","×💗×","×💖×",
    "×💝×","×💘×","×🩷×","×🤍×","×🩶×","×🖤×","🤎×","×💜×",
    "×💜×","×🩵×","×💛×","×🧡×","×❤️×","×🌼×","×🌻×","×🪻×",
"×🏵️×","×💮×","×🌸×","×🪷×","×🌷×",
    "×🌺×","×🥀×","×🌹×","×💐×","×💋×","×❤️‍🔥×","×❤️‍🩹×","×❣️×",
    "×♥️×","×💟×","×💌×","×💕×","×💞×","×💓×","×💗×","×💖×",
    "×💝×","×💘×","×🩷×","×🤍×","×🩶×","×🖤×","🤎×","×💜×",
    "×💜×","×🩵×","×💛×","×🧡×","×❤️×",
]

NCEMO_EMOJIS = [
  "😀","😃","😄","😁","😆","😅","😂","🤣","😭","😉","😗","😗","😚","😘","🥰","😍",
"🤩","🥳","🫠","🙃","🙂","🥲","🥹","😊","☺️","😌","🙂‍↕️","🙂‍↔️",
  "😏","🤤","😋","😛","😝","😜","🤪","🥴","😔","🥺","😬","😑","😐","😶","😶‍🌫️",
"🫥","🤐","🫡","🤔","🤫","🫢","🤭","🥱","🤗","🫣","😱","🤨","🧐","😒","🙄","😮‍💨","😤",
"😠","😡","🤬","😞","😓",
  "😟","😥","😢","☹️","🙁","🫤","😕","😰","😨","😧","😦","😮","😯","😲","😳",
  "🤯","😖","😣","😩","😵","😵‍💫","🫨","🥶","🥵","🤢","🤮","😴","😪","🤧","🤒",
  "🤒","🤕","😷","😇","🤠","🤑","🤓","😎","🥸",
]

ANI_EMOJIS = ["🐶","🐱","🐭","🐹","🐰","🦊","🐻","🐼","🐨","🐯","🦁","🐮","🐷","🐸","🐵","🐔","🐧","🐦","🐤","🐣","🦅","🦆","🦢","🦉","🐴","🦄","🐝","🪱","🐛","🦋","🐌","🐞","🐜","🦟","🦗","🕷","🕸","🦂","🐢","🐍","🦎","🦖","🦕","🐙","🦑","🦐","🦞","🦀","🐡","🐠","🐟","🐬","🐳","🐋","🦈","🐊","🐅","🐆","🦓","🦍","🦧","🐘","🦛","🦏","🐪","🐫","🦒","🦘","🦬","🐃","🐄","🐎","🐖","🐏","🐑","🐐","🦌","🐕","🐩","🦮","🐈","🐕‍🦺","🐓","🦃","🦚","🦜","🦢","🦩","🕊","🐇","🦝","🦨","🦡","🦦","🦥","🐁","🐀","🐿","🦔"]

FLAG_EMOJIS = ["🏁","🚩","🎌","🏴","🏳️","🏳️‍🌈","🏳️‍⚧️","🇦🇫","🇦🇱","🇩🇿","🇦🇸","🇦🇩","🇦🇴","🇦🇮","🇦🇶","🇦🇬","🇦🇷","🇦🇲","🇦🇼","🇦🇺","🇦🇹","🇦🇿","🇧🇸","🇧🇭","🇧🇩","🇧🇧","🇧🇾","🇧🇪","🇧🇿","🇧🇯","🇧🇲","🇧🇹","🇧🇴","🇧🇦","🇧🇼","🇧🇷","🇮🇴","🇻🇬","🇧🇳","🇧🇬","🇧🇫","🇧🇮","🇰🇭","🇨🇲","🇨🇦","🇮🇨","🇨🇻","🇧🇶","🇰🇾","🇨🇫","🇹🇩","🇨🇱","🇨🇳","🇨🇽","🇨🇨","🇨🇴","🇰🇲","🇨🇬","🇨🇩","🇨🇰","🇨🇷","🇨🇮","🇭🇷","🇨🇺","🇨🇼","🇨🇾","🇨🇿","🇩🇰","🇩🇯","🇩🇲","🇩🇴","🇪🇨","🇪🇬","🇸🇻","🇬🇶","🇪🇷","🇪🇪","🇪🇹","🇪🇺","🇫🇰","🇫🇴","🇫🇯","🇫🇮","🇫🇷","🇬🇫","🇵🇫","🇹🇫","🇬🇦","🇬🇲","🇬🇪","🇩🇪","🇬🇭","🇬🇮","🇬🇷","🇬🇱","🇬🇩","🇬🇵","🇬🇺","🇬🇹","🇬🇬","🇬🇳","🇬🇼","🇬🇾","🇭🇹","🇭🇳","🇭🇰","🇭🇺","🇮🇸","🇮🇳","🇮🇩","🇮🇷","🇮🇶","🇮🇪","🇮🇲","🇮🇱","🇮🇹","🇯🇲","🇯🇵","🇯🇪","🇯🇴","🇰🇿","🇰🇪","🇰🇮","🇽🇰","🇰🇼","🇰🇬","🇱🇦","🇱🇻","🇱🇧","🇱🇸","🇱🇷","🇱🇾","🇱🇮","🇱🇹","🇱🇺","🇲🇴","🇲🇰","🇲🇬","🇲🇼","🇲🇾","🇲🇻","🇲🇱","🇲🇹","🇲🇭","🇲🇶","🇲🇷","🇲🇺","🇾🇹","🇲🇽","🇫🇲","🇲🇩","🇲🇨","🇲🇳","🇲🇪","🇲🇸","🇲🇦","🇲🇿","🇲🇲","🇳🇦","🇳🇷","🇳🇵","🇳🇱","🇳🇨","🇳🇿","🇳🇮","🇳🇪","🇳🇬","🇳🇺","🇳🇫","🇰🇵","🇲🇵","🇳🇴","🇴🇲","🇵🇰","🇵🇼","🇵🇸","🇵🇦","🇵🇬","🇵🇾","🇵🇪","🇵🇭","🇵🇳","🇵🇱","🇵🇹","🇵🇷","🇶🇦","🇷🇪","🇷🇴","🇷🇺","🇷🇼","🇼🇸","🇸🇲","🇸🇹","🇸🇦","🇸🇳","🇷🇸","🇸🇨","🇸🇱","🇸🇬","🇸🇽","🇸🇰","🇸🇮","🇬🇸","🇸🇧","🇸🇴","🇿🇦","🇰🇷","🇸🇸","🇪🇸","🇱🇰","🇧🇱","🇸🇭","🇰🇳","🇱🇨","🇵🇲","🇻🇨","🇸🇩","🇸🇷","🇸🇿","🇸🇪","🇨🇭","🇸🇾","🇹🇼","🇹🇯","🇹🇿","🇹🇭","🇹🇱","🇹🇬","🇹🇰","🇹🇴","🇹🇹","🇹🇳","🇹🇷","🇹🇲","🇹🇨","🇹🇻","🇻🇮","🇺🇬","🇺🇦","🇦🇪","🇬🇧","🇺🇸","🇺🇾","🇺🇿","🇻🇺","🇻🇦","🇻🇪","🇻🇳","🇼🇫","🇪🇭","🇾🇪","🇿🇲","🇿🇼"]

HEART_EMOJIS = ["❤️","🧡","💛","💚","💙","💜","🖤","🤍","🤎","💔","❣️","💕","💞","💓","💗","💖","💘","💝","💟","❤️‍🔥","❤️‍🩹","🏩","💒","💌"]

KISS_EMOJIS = ["😘","😗","😚","😙","💋","👄","💏","👩‍❤️‍💋‍👨","👨‍❤️‍💋‍👨","👩‍❤️‍💋‍👩","🫦","💌","💘","💝"]

MOON_EMOJIS = ["🌑","🌒","🌓","🌔","🌕","🌖","🌗","🌘","🌙","🌚","🌛","🌜","☀️","🌝","🌕"]

# ---------------------------
# GLOBAL STATE
# ---------------------------
if os.path.exists(SUDO_FILE):
    try:
        with open(SUDO_FILE, "r") as f:
            _loaded = json.load(f)
            SUDO_USERS = set(int(x) for x in _loaded)
    except Exception:
        SUDO_USERS = {OWNER_ID}
else:
    SUDO_USERS = {OWNER_ID}

# Initialize data files
if os.path.exists(STICKER_FILE):
    try:
        with open(STICKER_FILE, "r") as f:
            user_stickers = json.load(f)
    except:
        user_stickers = {}
else:
    user_stickers = {}

if os.path.exists(VOICE_CLONES_FILE):
    try:
        with open(VOICE_CLONES_FILE, "r") as f:
            voice_clones = json.load(f)
    except:
        voice_clones = {}
else:
    voice_clones = {}

def save_sudo():
    with open(SUDO_FILE, "w") as f: 
        json.dump(list(SUDO_USERS), f)

def save_stickers():
    with open(STICKER_FILE, "w") as f: 
        json.dump(user_stickers, f)

def save_voice_clones():
    with open(VOICE_CLONES_FILE, "w") as f: 
        json.dump(voice_clones, f)

# Global state variables
group_tasks = {}         
spam_tasks = {}
react_tasks = {}
active_reactions = {}  # {chat_id: emoji}
photo_tasks = {} # {chat_id: task}
chat_photos = {} # {chat_id: [file_id]}
slide_targets = set()    
slidespam_targets = set()
exonc_tasks = {}
sticker_mode = True
apps, bots = [], []
delay = 0.001
spam_delay = 0.5
exonc_delay = 0.001

logging.basicConfig(level=logging.INFO)

# ---------------------------
# PHOTO LOOP
# ---------------------------
async def photo_loop(bot, chat_id, photos):
    i = 0
    while True:
        try:
            # Sync: always use latest file_id from the list
            if chat_id not in chat_photos or not chat_photos[chat_id]:
                await asyncio.sleep(1.0)
                continue
            
            # Use random choice to mix photos every time
            photos_list = chat_photos[chat_id]
            file_id = random.choice(photos_list)
            
            # Fetch fresh bytes to avoid cached issues
            photo_file = await bot.get_file(file_id)
            buf = io.BytesIO()
            await photo_file.download_to_memory(buf)
            buf.seek(0)
            
            # Setting new photo automatically removes the old one in Telegram groups
            await bot.set_chat_photo(chat_id=chat_id, photo=buf)
            
            await asyncio.sleep(0.1)
        except telegram.error.RetryAfter as e:
            await asyncio.sleep(e.retry_after + 1)
        except Exception as e:
            logging.error(f"Photo change error: {e}")
            await asyncio.sleep(1.0)

# ---------------------------
# DECORATORS
# ---------------------------
def only_sudo(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if uid not in SUDO_USERS:
            await update.message.reply_text("🐕❌𝑹𝑰𝑺𝑯𝑰~♤ PAPA SE SUDO LE PEHLE ❌.")
            return
        return await func(update, context)
    return wrapper

def only_owner(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if uid != OWNER_ID:
            await update.message.reply_text("🤬 SUDO DE DUNGA PHELE 𝑹𝑰𝑺𝑯𝑰~♤ KO PAPA BOLDE🤬.")
            return
        return await func(update, context)
    return wrapper

# ---------------------------
# tempest VOICE FUNCTIONS
# ---------------------------
async def generate_tempest_voice(text, voice_id, stability=0.1, similarity_boost=0.8):
    """Generate voice using tempest API"""
    url = f"https://api.tempest.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": tempest_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return io.BytesIO(response.content)
        else:
            logging.error(f"tempest API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logging.error(f"tempest request failed: {e}")
        return None

async def generate_multiple_voices(text, character_numbers):
    """Generate voices for multiple characters"""
    voices = []
    
    for char_num in character_numbers:
        if char_num in VOICE_CHARACTERS:
            voice_data = VOICE_CHARACTERS[char_num]
            audio_data = await generate_tempest_voice(text, voice_data["voice_id"])
            if audio_data:
                voices.append({
                    "character": voice_data["name"],
                    "audio": audio_data,
                    "description": voice_data["description"]
                })
    
    return voices

# ---------------------------
# LOOP FUNCTIONS
# ---------------------------
async def time_loop(bot, chat_id, base):
    """Indian Time based name changer loop - Smooth & Fast IST with MS"""
    ist_offset = timezone(timedelta(hours=5, minutes=30))
    while True:
        try:
            now = datetime.now(timezone.utc).astimezone(ist_offset)
            time_str = now.strftime("%H:%M:%S") + f":{now.microsecond // 10000:02d}"
            await bot.set_chat_title(chat_id, f"{base} {time_str}")
            # No sleep for maximum speed
        except Exception:
            await asyncio.sleep(0.1)

async def bot_loop(bot, chat_id, base, mode):
    i = 0
    while True:
        try:
            emoji = ""
            text = ""
            if mode == "gcnc":
                text = f"{base} {RAID_TEXTS[i % len(RAID_TEXTS)]}"
            elif mode == "ncemo":
                emoji = NCEMO_EMOJIS[i % len(NCEMO_EMOJIS)]
            elif mode == "ncemoani":
                emoji = ANI_EMOJIS[i % len(ANI_EMOJIS)]
            elif mode == "ncemoflag":
                emoji = FLAG_EMOJIS[i % len(FLAG_EMOJIS)]
            elif mode == "ncemoheart":
                emoji = HEART_EMOJIS[i % len(HEART_EMOJIS)]
            elif mode == "ncemokiss":
                emoji = KISS_EMOJIS[i % len(KISS_EMOJIS)]
            elif mode == "ncemomoon":
                emoji = MOON_EMOJIS[i % len(MOON_EMOJIS)]
            
            if emoji:
                text = f"{emoji} {base} {emoji}"
            
            if text:
                await bot.set_chat_title(chat_id, text)
            i += 1
            await asyncio.sleep(max(0.1, delay))
        except telegram.error.RetryAfter as e:
            await asyncio.sleep(e.retry_after + 1)
        except Exception:
            await asyncio.sleep(1.0)

async def ncbaap_loop(bot, chat_id, base):
    i = 0
    while True:
        try:
            emo1 = NCEMO_EMOJIS[i % len(NCEMO_EMOJIS)]
            emo2 = exonc_TEXTS[i % len(exonc_TEXTS)]
            patterns = [
                f"{base} {RAID_TEXTS[i % len(RAID_TEXTS)]}",
                f"{emo1} {base} {emo1}",
                f"{emo2} {base} {emo2}",
            ]
            for p in patterns:
                await bot.set_chat_title(chat_id, p)
                await asyncio.sleep(0.1) # Minimum safe interval
            i += 1
            await asyncio.sleep(max(0.1, delay))
        except telegram.error.RetryAfter as e:
            await asyncio.sleep(e.retry_after + 1)
        except Exception:
            await asyncio.sleep(1.0)

async def spam_loop(bot, chat_id, text):
    while True:
        try:
            await bot.send_message(chat_id, text)
            await asyncio.sleep(spam_delay)
        except Exception:
            await asyncio.sleep(0.1)

async def exonc_godspeed_loop(bot, chat_id, base_text):
    i = 0
    while True:
        try:
            patterns = [
                f"{base_text} {exonc_TEXTS[i % len(exonc_TEXTS)]}",
                f"{exonc_TEXTS[i % len(exonc_TEXTS)]} {base_text}",
            ]
            for p in patterns:
                await bot.set_chat_title(chat_id, p)
            i += 1
            await asyncio.sleep(0.01)
        except Exception:
            await asyncio.sleep(0.1)

async def exonc_loop(bot, chat_id, base_text):
    i = 0
    while True:
        try:
            emo = exonc_TEXTS[i % len(exonc_TEXTS)]
            await bot.set_chat_title(chat_id, f"{emo} {base_text} {emo}")
            i += 1
            await asyncio.sleep(exonc_delay)
        except Exception:
            await asyncio.sleep(0.1)

# ---------------------------
# CORE COMMANDS
# ---------------------------
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("𝑹𝑰𝑺𝑯𝑰~♤ TG NC— Commands 🪷\nUse +help")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "┏━━━━━━━━━━━━┓\n"
        "┃    𝑹𝑰𝑺𝑯𝑰  POOKIE 🎀  💖┃\n"
        "┗━━━━━━━━━━━━┛\n\n"
        "✦ 𝐍𝐂: +gcnc +ncemo +nctime\n"
        "✦ 𝐄𝐌𝐎𝐉𝐈+: +ncemoani +ncemoflag +ncemoheart +ncemokiss +ncemomoon\n"
        "✦ 𝐒𝐏𝐄𝐄𝐃: +ncbaap +exoncgodspeed\n"
        "✦ 𝐒𝐏𝐀𝐌: +spam +unspam\n"
        "✦ 𝐑𝐄𝐀𝐂𝐓: +emojispam +stopemojispam\n"
        "✦ 𝐒𝐋𝐈𝐃𝐄: +targetslide +slidespam\n"
        "✦ 𝐏𝐇𝐎𝐓𝐎: +savephoto +startphoto +stopphoto\n"
        "✦ 𝐌𝐈𝐒𝐂: +newsticker +animevn +ready\n\n"
        "✨ 𝐒𝐓𝐎𝐏 𝐀𝐋𝐋: +stopall ✨"
    )
    await update.message.reply_text(help_text)

async def ready_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start = time.time()
    msg = await update.message.reply_text("💭 Hmm...")
    end = time.time()
    await msg.edit_text(f"✅ All set! ")

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Your ID: {update.effective_user.id}")

# ---------------------------
# NAME CHANGER COMMANDS
# ---------------------------
@only_sudo
async def gcnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /gcnc <name>")
    
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    
    # Stop existing tasks
    if chat_id in group_tasks:
        for task in group_tasks[chat_id]:
            task.cancel()
    
    # Start new tasks
    tasks = []
    for bot in bots:
        task = asyncio.create_task(bot_loop(bot, chat_id, base, "gcnc"))
        tasks.append(task)
    
    group_tasks[chat_id] = tasks
    await update.message.reply_text("🔄 Started GC Name Changer!")

@only_sudo
async def ncemo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /ncemo <name>")
    
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    
    # Stop existing tasks
    if chat_id in group_tasks:
        for task in group_tasks[chat_id]:
            task.cancel()
    
    # Start new tasks
    tasks = []
    for bot in bots:
        task = asyncio.create_task(bot_loop(bot, chat_id, base, "ncemo"))
        tasks.append(task)
    
    group_tasks[chat_id] = tasks
    await update.message.reply_text("🌹 Emoji cycle started!")

@only_sudo
async def nctime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /nctime <name>")
    
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    
    # Stop existing tasks
    if chat_id in group_tasks:
        for task in group_tasks[chat_id]:
            task.cancel()
    
    # Start new tasks
    tasks = []
    for bot in bots:
        task = asyncio.create_task(time_loop(bot, chat_id, base))
        tasks.append(task)
    
    group_tasks[chat_id] = tasks
    await update.message.reply_text(f"🕒 Time loop started: {base} (HH:MM:SS:MS)")

@only_sudo
async def stopnctime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in group_tasks:
        for task in group_tasks[chat_id]:
            task.cancel()
        del group_tasks[chat_id]
        await update.message.reply_text("⏹ Time Name Changer Stopped!")
    else:
        await update.message.reply_text("❌ No active time changer")

@only_sudo
async def ncbaap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """GOD LEVEL Name Changer - 5 changes in 0.1 seconds"""
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /ncbaap <name>")
    
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    
    # Stop existing tasks
    if chat_id in group_tasks:
        for task in group_tasks[chat_id]:
            task.cancel()
    
    # Start ultra fast tasks
    tasks = []
    for bot in bots:
        task = asyncio.create_task(ncbaap_loop(bot, chat_id, base))
        tasks.append(task)
    
    group_tasks[chat_id] = tasks
    await update.message.reply_text("💀🔥 GOD SPEED NCBAAP LOOP STARTED  BY UR DAD 𝑹𝑰𝑺𝑯𝑰 💀🔥")

@only_sudo
async def stopgcnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in group_tasks:
        for task in group_tasks[chat_id]:
            task.cancel()
        del group_tasks[chat_id]
        await update.message.reply_text("⏹ GC Name Changer Stopped!")
    else:
        await update.message.reply_text("❌ No active GC changer")

@only_sudo
async def stopncemo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in group_tasks:
        for task in group_tasks[chat_id]:
            task.cancel()
        del group_tasks[chat_id]
        await update.message.reply_text("⏹ Emoji Name Changer Stopped!")
    else:
        await update.message.reply_text("❌ No active emoji changer")

@only_sudo
async def ncemoani(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /ncemoani <name>")
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    if chat_id in group_tasks:
        for task in group_tasks[chat_id]:
            task.cancel()
    tasks = []
    for bot in bots:
        task = asyncio.create_task(bot_loop(bot, chat_id, base, "ncemoani"))
        tasks.append(task)
    group_tasks[chat_id] = tasks
    await update.message.reply_text("🐾 Animal emoji cycle started!")

@only_sudo
async def ncemoflag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /ncemoflag <name>")
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    if chat_id in group_tasks:
        for task in group_tasks[chat_id]:
            task.cancel()
    tasks = []
    for bot in bots:
        task = asyncio.create_task(bot_loop(bot, chat_id, base, "ncemoflag"))
        tasks.append(task)
    group_tasks[chat_id] = tasks
    await update.message.reply_text("🚩 Flag emoji cycle started!")

@only_sudo
async def ncemoheart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /ncemoheart <name>")
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    if chat_id in group_tasks:
        for task in group_tasks[chat_id]:
            task.cancel()
    tasks = []
    for bot in bots:
        task = asyncio.create_task(bot_loop(bot, chat_id, base, "ncemoheart"))
        tasks.append(task)
    group_tasks[chat_id] = tasks
    await update.message.reply_text("❤️ Heart emoji cycle started!")

@only_sudo
async def ncemokiss(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /ncemokiss <name>")
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    if chat_id in group_tasks:
        for task in group_tasks[chat_id]:
            task.cancel()
    tasks = []
    for bot in bots:
        task = asyncio.create_task(bot_loop(bot, chat_id, base, "ncemokiss"))
        tasks.append(task)
    group_tasks[chat_id] = tasks
    await update.message.reply_text("😘 Kiss emoji cycle started!")

@only_sudo
async def ncemomoon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /ncemomoon <name>")
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    if chat_id in group_tasks:
        for task in group_tasks[chat_id]:
            task.cancel()
    tasks = []
    for bot in bots:
        task = asyncio.create_task(bot_loop(bot, chat_id, base, "ncemomoon"))
        tasks.append(task)
    group_tasks[chat_id] = tasks
    await update.message.reply_text("🌙 Moon emoji cycle started!")

@only_sudo
async def stopncbaap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in group_tasks:
        for task in group_tasks[chat_id]:
            task.cancel()
        del group_tasks[chat_id]
        await update.message.reply_text("⏹ GOD LEVEL NCBAAP Stopped!")
    else:
        await update.message.reply_text("❌ No active ncbaap")

# ---------------------------
# exonc COMMANDS - FIXED
# ---------------------------
@only_sudo
async def exonc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /exonc <name>")
    
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    
    # Stop existing tasks
    if chat_id in exonc_tasks:
        for task in exonc_tasks[chat_id]:
            task.cancel()
    
    # Start new tasks
    tasks = []
    for bot in bots:
        task = asyncio.create_task(exonc_loop(bot, chat_id, base))
        tasks.append(task)
    
    exonc_tasks[chat_id] = tasks
    await update.message.reply_text("💀 exonc Mode Activated!")

@only_sudo
async def exoncfast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global exonc_delay
    exonc_delay = 0.03
    
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /exoncfast <name>")
    
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    
    if chat_id in exonc_tasks:
        for task in exonc_tasks[chat_id]:
            task.cancel()
    
    tasks = []
    for bot in bots:
        task = asyncio.create_task(exonc_loop(bot, chat_id, base))
        tasks.append(task)
    
    exonc_tasks[chat_id] = tasks
    await update.message.reply_text("⚡ Faster exonc Activated!")

@only_sudo
async def exoncgodspeed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ULTRA FAST GOD SPEED MODE - FIXED"""
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /exoncgodspeed <name>")
    
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    
    # Stop existing tasks
    if chat_id in exonc_tasks:
        for task in exonc_tasks[chat_id]:
            task.cancel()
    
    # Start GOD SPEED tasks
    tasks = []
    for bot in bots:
        task = asyncio.create_task(exonc_godspeed_loop(bot, chat_id, base))
        tasks.append(task)
    
    exonc_tasks[chat_id] = tasks
    await update.message.reply_text("👑🔥 GOD SPEED exonc ACTIVATED! 10 NC in 0.01s! 🚀")

@only_sudo
async def stopexonc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in exonc_tasks:
        for task in exonc_tasks[chat_id]:
            task.cancel()
        del exonc_tasks[chat_id]
        await update.message.reply_text("🛑 exonc Stopped!")
    else:
        await update.message.reply_text("❌ No active exonc")

# ---------------------------
# SPAM COMMANDS
# ---------------------------
@only_sudo
async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /spam <text>")
    
    text = " ".join(context.args)
    chat_id = update.message.chat_id
    
    # Stop existing spam
    if chat_id in spam_tasks:
        for task in spam_tasks[chat_id]:
            task.cancel()
    
    # Use only one bot for spam to avoid conflicts and rate limits across multiple groups
    bot = random.choice(bots) if bots else None
    if not bot:
        return await update.message.reply_text("❌ No bots available")

    task = asyncio.create_task(spam_loop(bot, chat_id, text))
    spam_tasks[chat_id] = [task]
    
    await update.message.reply_text("💥 SPAM STARTED!")

@only_sudo
async def unspam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in spam_tasks:
        for task in spam_tasks[chat_id]:
            task.cancel()
        del spam_tasks[chat_id]
        await update.message.reply_text("🛑 Spam Stopped!")
    else:
        await update.message.reply_text("❌ No active spam")

# ---------------------------
# SLIDE COMMANDS - FIXED
# ---------------------------
@only_sudo
async def targetslide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to a user's message")
    
    target_id = update.message.reply_to_message.from_user.id
    slide_targets.add(target_id)
    await update.message.reply_text(f"🎯 Target slide added: {target_id}")

@only_sudo
async def stopslide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to a user's message")
    
    target_id = update.message.reply_to_message.from_user.id
    slide_targets.discard(target_id)
    await update.message.reply_text(f"🛑 Slide stopped: {target_id}")

@only_sudo
async def slidespam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to a user's message")
    
    target_id = update.message.reply_to_message.from_user.id
    slidespam_targets.add(target_id)
    await update.message.reply_text(f"💥 Slide spam started: {target_id}")

@only_sudo
async def stopslidespam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to a user's message")
    
    target_id = update.message.reply_to_message.from_user.id
    slidespam_targets.discard(target_id)
    await update.message.reply_text(f"🛑 Slide spam stopped: {target_id}")

# ---------------------------
# VOICE COMMANDS - tempest INTEGRATION
# ---------------------------
@only_sudo
async def animevn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Anime voice with tempest - FIXED SYNTAX"""
    if len(context.args) < 2:
        return await update.message.reply_text("⚠️ Usage: /animevn <character_numbers> <text>\nExample: /animevn 1 2 3 Hello world")
    
    try:
        # Parse character numbers
        char_numbers = []
        text_parts = []
        
        for arg in context.args:
            if arg.isdigit() and int(arg) in VOICE_CHARACTERS:
                char_numbers.append(int(arg))
            else:
                text_parts.append(arg)
        
        if not char_numbers:
            return await update.message.reply_text("❌ Please provide valid character numbers (1-10)")
        
        text = " ".join(text_parts)
        if not text:
            return await update.message.reply_text("❌ Please provide text to speak")
        
        await update.message.reply_text(f"🎭 Generating voices for characters: {', '.join([VOICE_CHARACTERS[num]['name'] for num in char_numbers])}...")
        
        # Generate voices
        voices = await generate_multiple_voices(text, char_numbers)
        
        if not voices:
            # Fallback to gTTS if tempest fails
            tts = gTTS(text=text, lang='ja', slow=False)
            voice_file = io.BytesIO()
            tts.write_to_fp(voice_file)
            voice_file.seek(0)
            
            character_names = [VOICE_CHARACTERS[num]['name'] for num in char_numbers]
            await update.message.reply_voice(
                voice=voice_file, 
                caption=f"🎀 {' + '.join(character_names)}: {text}"
            )
        else:
            # Send each voice
            for voice in voices:
                await update.message.reply_voice(
                    voice=voice["audio"],
                    caption=f"🎀 {voice['character']}: {text}\n{voice['description']}"
                )
                await asyncio.sleep(1)  # Delay between voices
        
    except Exception as e:
        await update.message.reply_text(f"❌ Voice error: {e}")

@only_sudo
async def tempest_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Default tempest voice"""
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /tempest <text>")
    
    text = " ".join(context.args)
    
    # Use Urokodaki voice as default
    audio_data = await generate_tempest_voice(text, VOICE_CHARACTERS[1]["voice_id"])
    
    if audio_data:
        await update.message.reply_voice(
            voice=audio_data,
            caption=f"🎙️ {VOICE_CHARACTERS[1]['name']}: {text}"
        )
    else:
        # Fallback to gTTS
        tts = gTTS(text=text, lang='en', slow=False)
        voice_file = io.BytesIO()
        tts.write_to_fp(voice_file)
        voice_file.seek(0)
        await update.message.reply_voice(voice=voice_file, caption=f"🗣️ Fallback TTS: {text}")

@only_sudo
async def voices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List available voices"""
    voice_list = "🎭 Available Anime Voices:\n\n"
    for num, voice in VOICE_CHARACTERS.items():
        voice_list += f"{num}. {voice['name']} - {voice['description']}\n"
    
    voice_list += "\n🎀 Usage: /animevn 1 2 3 Hello world"
    await update.message.reply_text(voice_list)

# Other voice commands remain the same...
@only_sudo
async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /music <song>")
    
    song = " ".join(context.args)
    await update.message.reply_text(f"🎶 Downloading: {song}")

@only_sudo
async def clonevn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to a voice message")
    
    await update.message.reply_text("🎤 Voice cloning started...")

@only_sudo
async def clonedvn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /clonedvn <text>")
    
    text = " ".join(context.args)
    await update.message.reply_text(f"🎙️ Speaking in cloned voice: {text}")

# ---------------------------
# REACT COMMANDS
# ---------------------------
@only_sudo
async def emojispam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /emojispam <emoji>")
    
    emoji = context.args[0]
    chat_id = update.message.chat_id
    
    active_reactions[chat_id] = emoji
    await update.message.reply_text(f"🎭 Auto-reaction started: {emoji}")

@only_sudo
async def stopemojispam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in active_reactions:
        del active_reactions[chat_id]
        await update.message.reply_text("🛑 Reactions Stopped!")
    else:
        await update.message.reply_text("❌ No active reactions")

# ---------------------------
# STICKER SYSTEM
# ---------------------------
@only_sudo
async def newsticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        return await update.message.reply_text("⚠️ Reply to a photo with /newsticker")
    
    await update.message.reply_text("✅ Sticker creation ready! Choose emoji for sticker")

@only_sudo
async def delsticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if str(user_id) in user_stickers:
        del user_stickers[str(user_id)]
        save_stickers()
        await update.message.reply_text("✅ Your stickers deleted!")
    else:
        await update.message.reply_text("❌ No stickers found")

@only_sudo
async def multisticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Creating 5 stickers...")

@only_sudo
async def stickerstatus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_stickers = sum(len(stickers) for stickers in user_stickers.values())
    await update.message.reply_text(f"📊 Sticker Status: {total_stickers} stickers total")

@only_owner
async def stopstickers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sticker_mode
    sticker_mode = False
    await update.message.reply_text("🛑 Stickers disabled")

@only_owner
async def startstickers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sticker_mode
    sticker_mode = True
    await update.message.reply_text("✅ Stickers enabled")

# ---------------------------
# CONTROL COMMANDS
# ---------------------------
@only_sudo
async def stopall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Stop all tasks
    for chat_tasks in group_tasks.values():
        for task in chat_tasks:
            task.cancel()
    group_tasks.clear()
    
    for chat_tasks in spam_tasks.values():
        for task in chat_tasks:
            task.cancel()
    spam_tasks.clear()
    
    for chat_tasks in react_tasks.values():
        for task in chat_tasks:
            task.cancel()
    react_tasks.clear()
    
    for chat_tasks in exonc_tasks.values():
        for task in chat_tasks:
            task.cancel()
    exonc_tasks.clear()
    
    slide_targets.clear()
    slidespam_targets.clear()
    
    await update.message.reply_text("⏹ ALL ACTIVITIES STOPPED!")

@only_sudo
async def delay_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global delay
    if not context.args:
        return await update.message.reply_text(f"⏱ Current delay: {delay}s")
    
    try:
        # Minimum speed 500ms (0.5s), Maximum speed 1ms (0.001s)
        new_delay = float(context.args[0])
        if new_delay < 0.001:
            new_delay = 0.001
        elif new_delay > 0.5:
            new_delay = 0.5
            
        delay = new_delay
        await update.message.reply_text(f"✅ Delay set to {delay}s (Range: 0.001s - 0.5s)")
    except:
        await update.message.reply_text("❌ Invalid number")

# ---------------------------
# STATUS COMMANDS
# ---------------------------
@only_sudo
async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_text = f"""
📊 𝑹𝑰𝑺𝑯𝑰~♤ :

🎀 Name Changers: {sum(len(tasks) for tasks in group_tasks.values())}
⚡ exonc Sessions: {sum(len(tasks) for tasks in exonc_tasks.values())}
😹 Spam Sessions: {sum(len(tasks) for tasks in spam_tasks.values())}
🪐 Reactions: {sum(len(tasks) for tasks in react_tasks.values())}
🪼 Slide Targets: {len(slide_targets)}
💥 Slide Spam: {len(slidespam_targets)}

⏱ Delay: {delay}s
⚡ exonc Delay: {exonc_delay}s
🤖 Active Bots: {len(bots)}
👑 SUDO Users: {len(SUDO_USERS)}
🎭 Voice Characters: {len(VOICE_CHARACTERS)}
    """
    await update.message.reply_text(status_text)

# ---------------------------
# SUDO MANAGEMENT
# ---------------------------
@only_owner
async def addsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to a user")
    
    uid = update.message.reply_to_message.from_user.id
    SUDO_USERS.add(uid)
    save_sudo()
    await update.message.reply_text(f"✅ SUDO added: {uid}")

@only_owner
async def delsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to a user")
    
    uid = update.message.reply_to_message.from_user.id
    if uid in SUDO_USERS:
        SUDO_USERS.remove(uid)
        save_sudo()
        await update.message.reply_text(f"🗑 SUDO removed: {uid}")
    else:
        await update.message.reply_text("❌ User not in SUDO")

@only_sudo
async def listsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sudo_list = "\n".join([f"👑 {uid}" for uid in SUDO_USERS])
    await update.message.reply_text(f"👑 SUDO Users:\n{sudo_list}")

@only_sudo
async def savephoto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        return await update.message.reply_text("⚠️ Reply to a photo to save it!")
    
    chat_id = update.message.chat_id
    file_id = update.message.reply_to_message.photo[-1].file_id
    
    if chat_id not in chat_photos:
        chat_photos[chat_id] = []
    
    chat_photos[chat_id].append(file_id)
    await update.message.reply_text(f"✅ Photo saved! Total: {len(chat_photos[chat_id])}")

@only_sudo
async def startphoto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id not in chat_photos or len(chat_photos[chat_id]) < 2:
        return await update.message.reply_text("⚠️ Save at least 2 photos first!")
    
    if chat_id in photo_tasks:
        photo_tasks[chat_id].cancel()
        
    bot = context.bot
    task = asyncio.create_task(photo_loop(bot, chat_id, chat_photos[chat_id]))
    photo_tasks[chat_id] = task
    await update.message.reply_text("🔄 Photo loop started (4s speed)!")

@only_sudo
async def stopphoto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in photo_tasks:
        photo_tasks[chat_id].cancel()
        del photo_tasks[chat_id]
        await update.message.reply_text("⏹ Photo loop stopped!")
    else:
        await update.message.reply_text("❌ No active photo loop")

@only_sudo
async def clearphotos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in chat_photos:
        del chat_photos[chat_id]
        await update.message.reply_text("🗑 Saved photos cleared!")

# ---------------------------
# AUTO REPLY HANDLER - FIXED
# ---------------------------
async def auto_replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.from_user:
        return

    uid = update.message.from_user.id
    chat_id = update.message.chat_id
    
    # Handle auto-reactions for EVERY message in enabled chats
    if chat_id in active_reactions:
        emoji = active_reactions[chat_id]
        try:
            # Pick a random bot to react
            bot = random.choice(bots) if bots else context.bot
            await bot.set_message_reaction(
                chat_id=chat_id,
                message_id=update.message.message_id,
                reaction=[{"type": "emoji", "emoji": emoji}],
                is_big=False
            )
            logging.info(f"✅ Reacted with {emoji} in chat {chat_id}")
        except Exception as e:
            logging.error(f"❌ Reaction failed in chat {chat_id}: {e}")

    # Handle slide targets
    if uid in slide_targets:
        for text in RAID_TEXTS[:3]:
            await update.message.reply_text(text)
            await asyncio.sleep(0.1)
    
    # Handle slidespam targets
    if uid in slidespam_targets:
        for text in RAID_TEXTS:
            await update.message.reply_text(text)
            await asyncio.sleep(0.05)

# ---------------------------
# BOT SETUP
# ---------------------------
def build_app(token):
    # Setup custom prefix
    from telegram.ext import PrefixHandler
    app = Application.builder().token(token).build()
    
    # Core commands
    app.add_handler(PrefixHandler("+", "start", start_cmd))
    app.add_handler(PrefixHandler("+", "help", help_cmd))
    app.add_handler(PrefixHandler("+", "ready", ready_cmd))
    app.add_handler(PrefixHandler("+", "myid", myid))
    app.add_handler(PrefixHandler("+", "status", status_cmd))
    
    # Name changer commands
    app.add_handler(PrefixHandler("+", "gcnc", gcnc))
    app.add_handler(PrefixHandler("+", "ncemo", ncemo))
    app.add_handler(PrefixHandler("+", "ncemoani", ncemoani))
    app.add_handler(PrefixHandler("+", "ncemoflag", ncemoflag))
    app.add_handler(PrefixHandler("+", "ncemoheart", ncemoheart))
    app.add_handler(PrefixHandler("+", "ncemokiss", ncemokiss))
    app.add_handler(PrefixHandler("+", "ncemomoon", ncemomoon))
    app.add_handler(PrefixHandler("+", "nctime", nctime))
    app.add_handler(PrefixHandler("+", "ncbaap", ncbaap))
    app.add_handler(PrefixHandler("+", "stopgcnc", stopgcnc))
    app.add_handler(PrefixHandler("+", "stopncemo", stopncemo))
    app.add_handler(PrefixHandler("+", "stopnctime", stopnctime))
    app.add_handler(PrefixHandler("+", "stopncbaap", stopncbaap))
    app.add_handler(PrefixHandler("+", "stopall", stopall))
    app.add_handler(PrefixHandler("+", "delay", delay_cmd))
    
    # exonc commands
    app.add_handler(PrefixHandler("+", "exonc", exonc))
    app.add_handler(PrefixHandler("+", "exoncfast", exoncfast))
    app.add_handler(PrefixHandler("+", "exoncgodspeed", exoncgodspeed))
    app.add_handler(PrefixHandler("+", "stopexonc", stopexonc))
    
    # Spam commands
    app.add_handler(PrefixHandler("+", "spam", spam))
    app.add_handler(PrefixHandler("+", "unspam", unspam))
    
    # React commands
    app.add_handler(PrefixHandler("+", "emojispam", emojispam))
    app.add_handler(PrefixHandler("+", "stopemojispam", stopemojispam))
    
    # Slide commands
    app.add_handler(PrefixHandler("+", "targetslide", targetslide))
    app.add_handler(PrefixHandler("+", "stopslide", stopslide))
    app.add_handler(PrefixHandler("+", "slidespam", slidespam))
    app.add_handler(PrefixHandler("+", "stopslidespam", stopslidespam))
    
    # Sticker commands
    app.add_handler(PrefixHandler("+", "newsticker", newsticker))
    app.add_handler(PrefixHandler("+", "delsticker", delsticker))
    app.add_handler(PrefixHandler("+", "multisticker", multisticker))
    app.add_handler(PrefixHandler("+", "stickerstatus", stickerstatus))
    app.add_handler(PrefixHandler("+", "stopstickers", stopstickers))
    app.add_handler(PrefixHandler("+", "startstickers", startstickers))
    
    # Voice commands
    app.add_handler(PrefixHandler("+", "animevn", animevn))
    app.add_handler(PrefixHandler("+", "tempest", tempest_cmd))
    app.add_handler(PrefixHandler("+", "music", music))
    app.add_handler(PrefixHandler("+", "clonevn", clonevn))
    app.add_handler(PrefixHandler("+", "clonedvn", clonedvn))
    app.add_handler(PrefixHandler("+", "voices", voices))
    
    # SUDO management
    app.add_handler(PrefixHandler("+", "addsudo", addsudo))
    app.add_handler(PrefixHandler("+", "delsudo", delsudo))
    app.add_handler(PrefixHandler("+", "listsudo", listsudo))
    
    # Photo loop commands
    app.add_handler(PrefixHandler("+", "savephoto", savephoto))
    app.add_handler(PrefixHandler("+", "startphoto", startphoto))
    app.add_handler(PrefixHandler("+", "stopphoto", stopphoto))
    app.add_handler(PrefixHandler("+", "clearphotos", clearphotos))
    
    # Auto reply handler for reactions and targets
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, auto_replies), group=1)
    
    return app

async def run_all_bots():
    # Start all bots
    unique_tokens = list(set(t.strip() for t in TOKENS if t.strip()))
    for token in unique_tokens:
        try:
            app = build_app(token)
            apps.append(app)
            bots.append(app.bot)
            await app.initialize()
            await app.start()
            await app.updater.start_polling()
            print(f"🚀 Bot started: {token[:10]}...")
        except Exception as e:
            print(f"❌ Failed starting bot: {e}")

    print(f"🎉 Exorcist V4 Ultra Multi is running with {len(bots)} bots!")
    print("📊 Chat ID:", CHAT_ID)
    print("🤖 Active Bots:", len(bots))
    print("💀 NCBAAP Mode: READY (10 NC in 0.1s)")
    print("👑 GOD SPEED Mode: READY (10 NC in 0.05s)")
    print("🎭 tempest Voices: ✅ ACTIVE WITH YOUR API KEY")
    print("⚡ All Features: ACTIVATED")
    
    # Keep running
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(run_all_bots())
    except KeyboardInterrupt:
        print("\n🛑 Kento V4 Shutting Down...")
    except Exception as e:
        print(f"❌ Error: {e}")

#MADE BY 𝑹𝑰𝑺𝑯𝑰~♤ PAPA 🙂