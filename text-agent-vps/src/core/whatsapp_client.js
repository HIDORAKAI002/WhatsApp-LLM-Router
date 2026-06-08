const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const brainService = require('../services/brain_service');
const fs = require('fs');

class WhatsAppClient {
    constructor() {
        this.client = new Client({
            authStrategy: new LocalAuth({ dataPath: './whatsapp_auth' }),
            puppeteer: { args: ['--no-sandbox', '--disable-setuid-sandbox'] }
        });

        this.initializeEvents();
    }

    initializeEvents() {
        this.client.on('qr', (qr) => {
            console.log('SCAN THIS QR CODE TO LINK WHATSAPP:');
            qrcode.generate(qr, { small: true });
        });

        this.client.on('ready', () => {
            console.log('WhatsApp Web Client is READY!');
        });

        this.client.on('message', async (msg) => {
            if (msg.from === 'status@broadcast') return;
            if (msg.hasMedia) return;

            console.log(`Received text from ${msg.from}: ${msg.body}`);
            await brainService.forwardMessage(msg.from, msg.body, msg._data.notifyName);
        });
    }

    async sendMessage(chatId, text) {
        await this.client.sendMessage(chatId, text);
        console.log(`Successfully replied to ${chatId}`);
    }

    async sendVoiceNote(chatId, filePath) {
        if (!fs.existsSync(filePath)) {
            throw new Error(`File not found: ${filePath}`);
        }
        const media = MessageMedia.fromFilePath(filePath);
        await this.client.sendMessage(chatId, media, { sendAudioAsVoice: true });
        console.log(`Voice note successfully uploaded to ${chatId}`);
    }

    start() {
        this.client.initialize();
    }
}

module.exports = new WhatsAppClient();
