const axios = require('axios');
const config = require('../config/env');

class BrainService {
    async forwardMessage(chatId, text, senderName) {
        try {
            console.log(`Forwarding message to Brain: ${text}`);
            await axios.post(`${config.BRAIN_SERVER_URL}/webhook`, {
                chatId: chatId,
                text: text,
                senderName: senderName || 'User'
            });
        } catch (e) {
            console.error('Error forwarding message to Brain:', e.message);
        }
    }
}

module.exports = new BrainService();
