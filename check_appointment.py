#!/usr/bin/env python3
from quart import Quart, render_template, request, jsonify, websocket
from telegram import Bot
import asyncio
import logging
import os
from datetime import datetime
import aiohttp
import json

app = Quart(__name__)
appointment_checker = None
check_task = None
connected_websockets = set()

class AppointmentChecker:
    def __init__(self, bot_token, chat_id, selected_country, selected_city, frequency):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.selected_country = selected_country
        self.selected_city = selected_city
        self.frequency = frequency
        self.running = False
        self.bot = None
        
    async def initialize(self):
        self.bot = Bot(token=self.bot_token)
        
    async def start_checking(self):
        self.running = True
        while self.running:
            try:
                await self.check_appointments()
                await asyncio.sleep(self.frequency * 60)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Error during appointment check: {e}")
                await asyncio.sleep(60)
                
    async def stop_checking(self):
        self.running = False
            
    async def check_appointments(self):
        API_URL = "https://api.schengenvisaappointments.com/api/visa-list/?format=json"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(API_URL) as response:
                    if response.status != 200:
                        raise Exception(f"API yanıt vermedi: {response.status}")
                    
                    appointments = await response.json()
                    available_appointments = []
                    
                    for appointment in appointments:
                        if (appointment['source_country'] == 'Turkiye' and 
                            appointment['mission_country'].lower() == self.selected_country.lower() and 
                            self.selected_city.lower() in appointment['center_name'].lower()):
                            
                            available_appointments.append({
                                'country': appointment['mission_country'],
                                'city': appointment['center_name'],
                                'date': appointment['appointment_date'],
                                'category': appointment['visa_category'],
                                'subcategory': appointment['visa_subcategory'],
                                'link': appointment['book_now_link']
                            })
                    
                    if available_appointments:
                        message = f"🎉 {self.selected_country} için randevu bulundu!\n\n"
                        for appt in available_appointments:
                            message += f"🏢 Merkez: {appt['city']}\n"
                            message += f"📅 Tarih: {appt['date']}\n"
                            message += f"📋 Kategori: {appt['category']}\n"
                            if appt['subcategory']:
                                message += f"📝 Alt Kategori: {appt['subcategory']}\n"
                            message += f"\n🔗 Randevu Linki:\n{appt['link']}\n\n"
                        
                        await self.bot.send_message(chat_id=self.chat_id, text=message)
                        # Send message to all connected websockets
                        for ws in connected_websockets:
                            try:
                                await ws.send(json.dumps({
                                    "type": "appointment",
                                    "message": message,
                                    "timestamp": datetime.now().strftime("%H:%M:%S")
                                }))
                            except Exception as e:
                                logging.error(f"WebSocket error: {e}")
                        return True
                    else:
                        # Send status update to websockets
                        for ws in connected_websockets:
                            try:
                                await ws.send(json.dumps({
                                    "type": "status",
                                    "message": f"Kontrol edildi: {self.selected_country} - {self.selected_city}",
                                    "timestamp": datetime.now().strftime("%H:%M:%S")
                                }))
                            except Exception as e:
                                logging.error(f"WebSocket error: {e}")
                    return False
                    
        except Exception as e:
            logging.error(f"API kontrolü sırasında hata: {str(e)}")
            return False

@app.websocket('/ws')
async def ws():
    connected_websockets.add(websocket._get_current_object())
    try:
        while True:
            await websocket.receive()
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
    finally:
        connected_websockets.remove(websocket._get_current_object())

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/start', methods=['POST'])
async def start_checking():
    global appointment_checker, check_task
    
    try:
        data = await request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Invalid JSON data"}), 400
            
        bot_token = data.get('bot_token')
        chat_id = data.get('chat_id')
        country = data.get('country')
        city = data.get('city')
        frequency = int(data.get('frequency', 5))
        
        if appointment_checker:
            await appointment_checker.stop_checking()
            
        appointment_checker = AppointmentChecker(bot_token, chat_id, country, city, frequency)
        await appointment_checker.initialize()
        
        check_task = asyncio.create_task(appointment_checker.start_checking())
        return jsonify({"status": "success", "message": "Randevu kontrolü başlatıldı"})
    except Exception as e:
        logging.error(f"Start error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/stop', methods=['POST'])
async def stop_checking():
    global appointment_checker, check_task
    
    try:
        if appointment_checker:
            await appointment_checker.stop_checking()
            appointment_checker = None
            
        if check_task:
            check_task.cancel()
            check_task = None
            
        return jsonify({"status": "success", "message": "Randevu kontrolü durduruldu"})
    except Exception as e:
        logging.error(f"Stop error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='127.0.0.1', port=5000) 